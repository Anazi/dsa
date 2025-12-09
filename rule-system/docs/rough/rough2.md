Absolutely—good catch on the naming. I’ve updated the design so the base repo’s filter file is **20-filter.conf** (leaving room for controlled user overlays like 15/25/35). Here’s the complete, cohesive doc with all changes folded in.

---

# **Logstash File Ingestion Framework – Runtime Pipeline Fetch Design**

This document defines the **standard architecture** for file ingestion into Kafka using **Logstash**, managed via **Helm-deployed per-business (biz) repositories**.
It cleanly separates **shared pipeline logic (base repo)** from **deployment ownership (biz repos)** while preserving version control, flexibility, and governance.

---

## **1. End-to-End Architecture**

### **1.1 High-Level Flow**

```
[Client Server (exports files via NFS/SFTP/HTTP)]
        ↓
[NFS or Sync Mount on Kubernetes PVC]
        ↓
[Logstash Pod (per-biz Helm deployment)]
   ├── InitContainer (fetches base pipelines from JFrog)
   ├── Optional PluginPack InitContainer
   └── Main Logstash Container (executes unified pipeline)
        ↓
[Kafka Topics (raw + DLQ)]
        ↓
[Downstream Consumers / Data Pipelines]
```

---

### **1.2 Repository and Artifact Layout**

```
logstash-pipelines-base/           (shared repo)
 ├─ pipelines/
 │   ├─ 01-input.conf
 │   ├─ 20-filter.conf           # <- renamed from 02 to leave room for 15/25/35 overlays
 │   ├─ 03-output.conf
 │   ├─ patterns/common.grok
 │   └─ README.md (contract + envs)
 └─ version.txt  (e.g., 1.3.0)
         │
         ▼  (published as tar.gz to JFrog)
JFrog Artifactory:
  acme-logstash-pipelines-base-1.3.0.tar.gz

logstash-<biz>/                    (per-biz repo)
 ├─ charts/logstash/               (Helm chart owned by biz)
 │   ├─ templates/statefulset.yaml
 │   ├─ templates/init-pipeline-fetch.yaml
 │   ├─ templates/init-plugins.yaml
 │   ├─ templates/service.yaml
 │   └─ values-*.yaml
 ├─ overlay-pipelines/             (optional, controlled)
 │   ├─ 15-prefilter.conf          # pre-parse slot
 │   ├─ 25-midfilter.conf          # post-parse slot
 │   └─ 35-postfilter.conf         # pre-output slot
 ├─ plugins/                       (offline packs if needed)
 └─ ci/ (fetch/verify/publish)
```

**Key principles**

* The **base repo** is versioned and publishes **only** pipeline templates.
* Each **biz repo**:

  * Owns deployment, environment configuration, and installers.
  * Fetches and mounts the **pipeline pack at runtime**.
  * Uses **overlay slots (15/25/35)** for safe extensions—**no overwriting** of base files.

---

## **2. Client-Side File Access (NFS Mount)**

### **2.1 Setup Overview**

Clients expose read-only folders using NFS for agentless file access.

#### **Steps (on client side)**

1. **Install NFS utilities**

```bash
sudo apt install -y nfs-kernel-server    # Ubuntu/Debian
# or
sudo yum install -y nfs-utils            # RHEL/CentOS
```

2. **Create and export directory**

```bash
sudo mkdir -p /data/export
sudo chown -R svc_nfs:svc_nfs /data/export
sudo chmod 755 /data/export
```

3. **Configure `/etc/exports`**

```bash
/data/export 10.20.30.0/24(ro,sync,root_squash,no_subtree_check)
```

4. **Apply export & enable service**

```bash
sudo exportfs -ra
sudo systemctl enable --now nfs-server rpcbind
```

5. **Open required ports**

* 2049/tcp,udp (NFS)
* 111/tcp,udp (rpcbind)

6. **Mount on Kubernetes (PV/PVC)**

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-client-orders
spec:
  capacity: { storage: 10Gi }
  accessModes: [ "ReadOnlyMany" ]
  nfs:
    path: /data/export/orders
    server: clienthost.example.com
  persistentVolumeReclaimPolicy: Retain
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-client-orders
spec:
  accessModes: [ "ReadOnlyMany" ]
  resources:
    requests: { storage: 10Gi }
  volumeName: pv-client-orders
```

---

## **3. Mount Mode Advantages**

* **Agentless ingestion:** no software on client systems.
* **Real-time visibility:** files appear on rename/move.
* **No duplication:** Logstash reads directly from the mount.
* **Atomic handoff compatible:** `.inprogress → final`.
* **Resilient:** automatic recovery after NFS reconnect.

---

## **4. Runtime Pipeline Fetch (InitContainer Design)**

### **4.1 Flow**

```
InitContainer: "pipeline-fetch"
    ↓ downloads tar.gz from JFrog (pinned version)
    ↓ extracts to /pipeline-base
    ↓ applies optional overlays from /overlay (15/25/35 only)
    ↓ copies final files to /usr/share/logstash/pipeline
Logstash main container
    ↓ starts with base + overlays
    ↓ executes pipeline (01 / 20 / 03)
```

### **4.2 Helm Snippet – InitContainer to Fetch Pipelines**

```yaml
initContainers:
- name: pipeline-fetch
  image: alpine:3.20
  command: ["/bin/sh", "-c"]
  args: >
    set -e;
    echo "Fetching pipelines version ${PIPELINE_VERSION}...";
    mkdir -p /pipeline-base &&
    wget -q -O /tmp/pipelines.tar.gz ${PIPELINE_URL}/${PIPELINE_VERSION}.tar.gz &&
    tar -xzf /tmp/pipelines.tar.gz -C /pipeline-base &&
    echo "Applying overlays (if any)..." &&
    # Only copy whitelisted overlay files to avoid base overwrite
    for f in 15-prefilter.conf 25-midfilter.conf 35-postfilter.conf; do
      if [ -f "/overlay/$f" ]; then cp -f "/overlay/$f" "/pipeline-base/$f"; fi
    done;
    echo "Pipelines ready.";
  env:
    - name: PIPELINE_VERSION
      value: "1.3.0"   # pin per biz
    - name: PIPELINE_URL
      value: "https://jfrog.io/artifactory/logstash-pipelines-base"
  volumeMounts:
    - name: pipeline-base
      mountPath: /pipeline-base
    - name: overlay
      mountPath: /overlay
volumes:
  - name: pipeline-base
    emptyDir: {}
  - name: overlay
    configMap:
      name: {{ include "ls.fullname" . }}-overlay
```

> The **pipeline-base** directory is then mounted into the main container at `/usr/share/logstash/pipeline`.
> **Overlay whitelist** ensures devs can’t overwrite `01/20/03`.

### **4.3 Optional Overlay ConfigMap (biz-specific)**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "ls.fullname" . }}-overlay
data:
  25-midfilter.conf: |
    # Example: convert amount → float after base parsing
    if [event][amount] { mutate { convert => { "[event][amount]" => "float" } } }
```

### **4.4 Main Container Mounts**

```yaml
volumeMounts:
  - name: pipeline-base
    mountPath: /usr/share/logstash/pipeline
  - name: pvc-client-orders
    mountPath: /mnt/inbox
```

---

## **5. Base Repo Pipeline Files (env-driven, no @metadata)**

> Biz repos **must** provide `FILE_FORMAT` in env: one of `csv` | `ndjson` | `json_whole` | `xml`.
> All choices (paths, CSV/JSON/XML options, Kafka, etc.) are supplied by **env vars** from the biz Helm chart.
> Overlays are **additive only** via `15/25/35` to avoid overwriting base.

### **5.1 `01-input.conf`**

```ruby
##
# 01-input.conf — file input (type-agnostic)
# Required env from biz:
#   WATCH_PATH     : glob to watch (e.g., /mnt/inbox/*.csv)
# Optional envs:
#   EXCLUDE_GLOB1/2, START_POS, SINCE_DB, MAX_OPEN_FILES, INPUT_CHARSET
##

input {
  file {
    path            => "${WATCH_PATH:/.disabled/*.none}"
    exclude         => ["${EXCLUDE_GLOB1:*.tmp}","${EXCLUDE_GLOB2:*.inprogress}"]
    start_position  => "${START_POS:beginning}"
    sincedb_path    => "${SINCE_DB:/var/lib/logstash/sincedb/since}"
    max_open_files  => ${MAX_OPEN_FILES:4096}
    mode            => "read"
    codec           => plain { charset => "${INPUT_CHARSET:UTF-8}" }
  }
}
```

### **5.2 `20-filter.conf`**  *(renamed as requested)*

```ruby
##
# 20-filter.conf — unified parsing + enrichment (env-driven)
#
# Required env from biz:
#   FILE_FORMAT           : csv | ndjson | json_whole | xml
# Optional envs (per format):
#   CSV_HEADER_AUTODETECT : true|false
#   CSV_SEPARATOR         : default ","
#   JSON_ROOT_ARRAY       : true|false (split if root is array)
#   JSON_EXTRACT          : dotted path to copy into [event][extracted]
#   XML_SPLIT_ENABLED     : true|false (prefer overlay with explicit xpath)
#
# Identity/env:
#   BIZ, FEED, SOURCE_SYSTEM
#
# Extension slots (biz provides these separate files; base never modified):
#   15-prefilter.conf   (runs BEFORE parsing branches)
#   25-midfilter.conf   (runs AFTER parsing, BEFORE DLQ tagging)
#   35-postfilter.conf  (runs AFTER midfilter, BEFORE outputs)
##

# -------- 15-prefilter.conf (biz overlay, optional) --------

filter {
  # ---------- Common enrichment ----------
  mutate {
    add_field => {
      "biz"            => "${BIZ:unknown}"
      "feed"           => "${FEED:unknown}"
      "source_system"  => "${SOURCE_SYSTEM:unknown}"
      "source_path"    => "%{path}"
      "ingested_at"    => "%{@timestamp}"
      "file_format"    => "${FILE_FORMAT:unknown}"
    }
  }

  # ---------- Switch by FILE_FORMAT ----------
  if "${FILE_FORMAT}" == "ndjson" {
    json { source => "message" target => "[event]" }
  }
  else if "${FILE_FORMAT}" == "json_whole" {
    json { source => "message" target => "[root]" }
    if [root] and "${JSON_ROOT_ARRAY:false}" == "true" and [root][0] {
      split { field => "[root]" }
      mutate { rename => { "[root]" => "[event]" } }
    } else {
      mutate { rename => { "[root]" => "[event]" } }
    }
    if "${JSON_EXTRACT:}" != "" {
      ruby {
        code => '
          path = ENV["JSON_EXTRACT"]
          v = event.get("[event]")
          if v && path
            value = path.split(".").reduce(v){|a,k| a.is_a?(Hash) ? a[k] : nil }
            event.set("[event][extracted]", value) unless value.nil?
          end
        '
      }
    }
  }
  else if "${FILE_FORMAT}" == "csv" {
    if "${CSV_HEADER_AUTODETECT:true}" == "true" {
      csv {
        separator               => "${CSV_SEPARATOR:,}"
        autodetect_column_names => true
        skip_empty_columns      => true
      }
    } else {
      # For explicit columns, supply a small overlay that sets:
      # csv { columns => ["c1","c2",...], separator => "${CSV_SEPARATOR:,}" }
      csv {
        separator               => "${CSV_SEPARATOR:,}"
        skip_empty_columns      => true
      }
    }
    # Move parsed flat fields under [event] to keep top-level clean
    ruby {
      code => '
        h = event.to_hash
        keep = {}
        h.each { |k,v|
          next if k.start_with?("@") || ["biz","feed","source_system","source_path","ingested_at","file_format"].include?(k)
          keep[k]=v
        }
        event.set("[event]", keep) unless keep.empty?
      '
    }
  }
  else if "${FILE_FORMAT}" == "xml" {
    xml {
      source            => "message"
      store_xml         => true
      target            => "[xml]"
      remove_namespaces => true
      force_content     => false
      # For complex schemas, add overlay with explicit xpath:
      # xml { xpath => [ "/root/record", "records" ] target => "xml" }
    }
    if [records] {
      split { field => "[records]" }
      mutate { rename => { "[records]" => "[event]" } }
    } else if [xml] {
      mutate { rename => { "[xml]" => "[event]" } }
    }
  }
  else {
    mutate { add_tag => ["unknown_format"] }
    mutate { add_field => { "[event][raw]" => "%{message}" } }
  }

  # -------- 25-midfilter.conf (biz overlay, optional) --------

  # Ensure [event] exists
  if ![event] {
    mutate { add_field => { "[event][raw]" => "%{message}" } }
  }

  # Optional fingerprint for idempotency
  if "${ENABLE_FINGERPRINT:true}" == "true" {
    fingerprint {
      method                 => "SHA1"
      key                    => "${FINGERPRINT_SALT:}"
      source                 => ["message","path","file_format"]
      target                 => "event_key"
      concatenate_sources    => true
    }
  }

  # Uniform parse failure tagging
  if "_jsonparsefailure" in [tags] or "_csvparsefailure" in [tags] or "_xmlparsefailure" in [tags] {
    mutate { add_tag => ["parse_error"] }
  }

  # -------- 35-postfilter.conf (biz overlay, optional) --------
}
```

### **5.3 `03-output.conf`**

```ruby
##
# 03-output.conf — Kafka routing (raw vs DLQ) + optional stdout
# Required env:
#   KAFKA_BOOTSTRAP
#   KAFKA_TOPIC           (raw)
# Optional:
#   DLQ_TOPIC, KAFKA_ACKS, KAFKA_COMPRESSION, KAFKA_IDEMPOTENCE, LOG_TO_STDOUT
##

output {
  # DLQ
  if "parse_error" in [tags] or "unknown_format" in [tags] {
    kafka {
      bootstrap_servers  => "${KAFKA_BOOTSTRAP:localhost:9092}"
      topic_id           => "${DLQ_TOPIC:dlq.${BIZ}.${FEED}}"
      acks               => "${KAFKA_ACKS:all}"
      compression_type   => "${KAFKA_COMPRESSION:lz4}"
      codec              => json
    }
  }
  # Normal publish
  else {
    kafka {
      bootstrap_servers  => "${KAFKA_BOOTSTRAP:localhost:9092}"
      topic_id           => "${KAFKA_TOPIC:raw.${BIZ}.${FEED}.v1}"
      acks               => "${KAFKA_ACKS:all}"
      compression_type   => "${KAFKA_COMPRESSION:lz4}"
      enable_idempotence => ${KAFKA_IDEMPOTENCE:true}
      codec              => json
    }
  }

  # Optional debug
  if "${LOG_TO_STDOUT:false}" == "true" {
    stdout { codec => rubydebug { metadata => false } }
  }
}
```

---

## **6. Plugin Management (Biz-Controlled)**

Use a **PluginPack InitContainer** to install approved plugins at runtime (no image rebuilds). Prefer offline packs from JFrog:

```yaml
initContainers:
- name: pluginpack
  image: alpine:3.20
  command: ["/bin/sh","-c"]
  args: >
    set -e;
    echo "Installing Logstash plugins...";
    mkdir -p /plugins &&
    wget -q -O /plugins/offline-pack.zip ${PLUGIN_URL} &&
    /usr/share/logstash/bin/logstash-plugin install file:///plugins/offline-pack.zip
  env:
    - name: PLUGIN_URL
      value: "https://jfrog.io/artifactory/logstash-plugins/offline-pack.zip"
  volumeMounts:
    - name: ls-home
      mountPath: /usr/share/logstash
    - name: plugins
      mountPath: /plugins
volumes:
  - name: ls-home
    emptyDir: {}
  - name: plugins
    emptyDir: {}
```

---

## **7. Helm Values Example (orders.csv)**

```yaml
image:
  repository: logstash:8.12.0
  pullPolicy: IfNotPresent

app:
  biz: "orders"
  feed: "daily-csv"

env:
  - name: FILE_FORMAT
    value: "csv"
  - name: WATCH_PATH
    value: "/mnt/inbox/*.csv"
  - name: KAFKA_BOOTSTRAP
    value: "kfk-1:9093,kfk-2:9093"
  - name: KAFKA_TOPIC
    value: "raw.orders.daily.v1"
  - name: BIZ
    value: "orders"
  - name: FEED
    value: "daily-csv"

nfs:
  pvc: "pvc-client-orders"
  mountPath: "/mnt/inbox"

pipeline:
  version: "1.3.0"
  url: "https://jfrog.io/artifactory/logstash-pipelines-base"

plugins:
  enabled: false

resources:
  requests: { cpu: 250m, memory: 512Mi }
  limits:   { cpu: 1,    memory: 1Gi  }
```

---

## **8. Governance & Versioning**

| Area               | Policy                                                                                             |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| **Base Pipelines** | Versioned (SemVer) to JFrog; biz repos **pin versions**.                                           |
| **Overlays**       | Only `15/25/35` allowed; **no overwrite** of `01/20/03`. Enforced in init script and CI policy.    |
| **Plugins**        | Must come from approved Artifactory; offline packs preferred.                                      |
| **Security**       | Read-only NFS; secrets via Vault/SealedSecrets.                                                    |
| **Schema**         | Biz charts include `values.schema.json` to validate required envs and enums (e.g., `FILE_FORMAT`). |
| **Audit**          | All changes via PRs (values/overlay files), plus artifact version pins.                            |
| **Promotion**      | DEV → PREPROD → PROD with pinned pipeline & plugin versions.                                       |

---

## **9. Onboarding Steps (New Biz)**

1. **Client:** Expose NFS read-only folder.
2. **Cluster:** Create PV/PVC to mount client export.
3. **Biz repo:**

   * Add pipeline-fetch InitContainer; pin `pipeline.version`.
   * Set required envs: `FILE_FORMAT`, `WATCH_PATH`, Kafka, identity.
   * (Optional) Add overlay files `15/25/35` for safe tweaks.
   * (Optional) Add PluginPack InitContainer if extra plugins needed.
4. **Deploy via Helm/ArgoCD**; validate ingestion; promote.

---

### ✅ Final takeaway

* **Base repo** supplies standardized, env-driven **01/20/03** pipelines.
* **Biz repos** never overwrite base files—only add **15/25/35** overlays.
* Pipelines are **fetched at runtime** (no ConfigMap size limits).
* **FILE_FORMAT** and all parsing choices come from **biz-provided envs**, keeping the system repeatable, modern, and resilient.

If you want, I can add a tiny example for `15/25/35` overlays tailored to CSV explicit columns or XML XPath splitting.
