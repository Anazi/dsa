

### `01-input.conf`

```ruby
##
# 01-input.conf — single file input (type-agnostic)
# Biz must provide:
#  - WATCH_PATH: glob of files to read (e.g., /mnt/inbox/*.csv)
#  - START_POS, SINCE_DB, EXCLUDE_GLOB*, MAX_OPEN_FILES (optional)
#  - FILE_FORMAT is NOT used here; parsing happens in 02-filter.conf
##

input {
  file {
    path            => "${WATCH_PATH:/.disabled/*.none}"
    exclude         => ["${EXCLUDE_GLOB1:*.tmp}","${EXCLUDE_GLOB2:*.inprogress}"]
    start_position  => "${START_POS:beginning}"
    sincedb_path    => "${SINCE_DB:/var/lib/logstash/sincedb/since}"
    max_open_files  => ${MAX_OPEN_FILES:4096}
    mode            => "read"

    # Multiline is file-type specific; if you truly need it at input,
    # set FILE_MULTILINE_MODE=true and tune patterns/env below.
    codec => plain {
      charset => "${INPUT_CHARSET:UTF-8}"
    }
  }
}
```

---

### `20-filter.conf`

```ruby
##
# 02-filter.conf — unified parsing + enrichment
#
# Biz must provide:
#  - FILE_FORMAT: "csv" | "ndjson" | "json_whole" | "xml"
#  - CSV_*, JSON_*, XML_* envs as needed (see branches below)
#  - Optional: ENABLE_FINGERPRINT, FINGERPRINT_SALT
#
# Extension slots (biz adds separate files in the same directory; DO NOT edit base files):
#  - 15-prefilter.conf   (runs BEFORE the parse branches below)
#  - 25-midfilter.conf   (runs AFTER parse, BEFORE DLQ tagging)
#  - 35-postfilter.conf  (runs AFTER midfilter, BEFORE outputs)
##

# --------- 15-prefilter.conf (biz-provided, optional) ---------
# Intentionally empty here; biz may supply a file named exactly "15-prefilter.conf"

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
    # Newline-delimited JSON (one JSON per line)
    json { source => "message" target => "[event]" }
  }
  else if "${FILE_FORMAT}" == "json_whole" {
    # Whole-file JSON (object OR array)
    # Option A: auto-detect array when JSON_ROOT_ARRAY=true
    json { source => "message" target => "[root]" }
    if [root] and "${JSON_ROOT_ARRAY:false}" == "true" and [root][0] {
      split { field => "[root]" }
      mutate { rename => { "[root]" => "[event]" } }
    } else {
      mutate { rename => { "[root]" => "[event]" } }
    }

    # Optional JSON field extraction (env-driven, best-effort):
    # Provide a dotted path to copy into event (e.g., JSON_EXTRACT=payload.orderId)
    if "${JSON_EXTRACT:}" != "" {
      ruby {
        code => '
          path = ENV["JSON_EXTRACT"]
          v = event.get("[event]") || event.get("[root]")
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
      # For explicit columns, prefer a small overlay file that sets:
      # csv { columns => ["col1","col2",...], separator => "${CSV_SEPARATOR:,}" }
      # (Arrays are hard to pass via env, so we keep base generic.)
      csv {
        separator               => "${CSV_SEPARATOR:,}"
        skip_empty_columns      => true
      }
    }

    # Wrap parsed flat fields under [event] to keep top-level clean
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
    # Multi-line XML: parse whole message
    xml {
      source            => "message"
      store_xml         => true
      target            => "[xml]"
      remove_namespaces => true
      force_content     => false
      # Complex schemas should be handled via a biz overlay using explicit xpath =>
      #   xml { xpath => [ "/root/record", "records" ] target => "xml" }
    }

    # Split per repeating node if [records] was produced (recommended via overlay with xpath)
    if [records] {
      split { field => "[records]" }
      mutate { rename => { "[records]" => "[event]" } }
    } else if [xml] {
      # Fallback: treat the XML doc as single event
      mutate { rename => { "[xml]" => "[event]" } }
    }
  }
  else {
    # Unknown format → keep raw
    mutate { add_tag => ["unknown_format"] }
    mutate { add_field => { "[event][raw]" => "%{message}" } }
  }

  # --------- 25-midfilter.conf (biz-provided, optional) ---------
  # Intentionally empty here; biz may supply a file named exactly "25-midfilter.conf"

  # ---------- Ensure [event] exists ----------
  if ![event] {
    mutate { add_field => { "[event][raw]" => "%{message}" } }
  }

  # ---------- Idempotency fingerprint (optional) ----------
  if "${ENABLE_FINGERPRINT:true}" == "true" {
    fingerprint {
      method        => "SHA1"
      key           => "${FINGERPRINT_SALT:}"
      source        => ["message","path","file_format"]
      target        => "event_key"
      concatenate_sources => true
    }
  }

  # ---------- Uniform parse failure tagging ----------
  if "_jsonparsefailure" in [tags] or "_csvparsefailure" in [tags] or "_xmlparsefailure" in [tags] {
    mutate { add_tag => ["parse_error"] }
  }

  # --------- 35-postfilter.conf (biz-provided, optional) ---------
  # Intentionally empty here; biz may supply a file named exactly "35-postfilter.conf"
}
```

---

### `03-output.conf`

```ruby
##
# 03-output.conf — Kafka routing (raw vs DLQ) + optional stdout
#
# Biz must provide:
#  - KAFKA_BOOTSTRAP
#  - KAFKA_TOPIC (raw topic)
#  - DLQ_TOPIC (optional; default uses biz/feed)
#  - KAFKA_ACKS, KAFKA_COMPRESSION, KAFKA_IDEMPOTENCE (optional)
#  - LOG_TO_STDOUT (optional)
##

output {
  # -------- DLQ for parse errors --------
  if "parse_error" in [tags] or "unknown_format" in [tags] {
    kafka {
      bootstrap_servers  => "${KAFKA_BOOTSTRAP:localhost:9092}"
      topic_id           => "${DLQ_TOPIC:dlq.${BIZ}.${FEED}}"
      acks               => "${KAFKA_ACKS:all}"
      compression_type   => "${KAFKA_COMPRESSION:lz4}"
      codec              => json
    }
  }
  # -------- Normal publish --------
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

  # -------- Optional debug to stdout --------
  if "${LOG_TO_STDOUT:false}" == "true" {
    stdout {
      codec => rubydebug { metadata => false }
    }
  }
}
```

---

## How biz repos extend safely (without overwriting base)

* Add **separate files** (same directory) using these exact names:

  * `15-prefilter.conf` (pre-parse tweaks: e.g., normalize delimiters)
  * `25-midfilter.conf` (post-parse enrich/validate)
  * `35-postfilter.conf` (route/headers/PII masks)
* Your Helm chart should **only allow** those filenames (policy/validation) and **forbid** creating or modifying `01/02/03` to prevent accidental overrides.
* For CSV explicit columns or XML XPath, put the specific `csv { columns => [...] }` or `xml { xpath => [...] }` in **your** `25-midfilter.conf` (or an additional `20-parse-overlay.conf` if you prefer), keeping the base files intact.

If you want, I can also give you tiny starter contents for those three extension files.
