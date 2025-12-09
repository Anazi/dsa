# 🧱 Low-Level Design (LLD) — `alerting-service`

```textmate
alerting-service/
├── pom.xml                                   # Spring Boot 3 + Kotlin + Web + Validation + JPA + GraphQL + Kafka + Actuator
└── src
    ├── main
    │   ├── kotlin/ca/bell/wireless/alerting
    │   │   ├── App.kt                        # @SpringBootApplication entrypoint
    │   │   ├── config/                       # Centralized Spring configs (no migrations)
    │   │   │   ├── AppConfig.kt              # ObjectMapper(Kotlin), Clock, Id generators, common beans
    │   │   │   ├── JPAConfig.kt              # H2-on-PVC JDBC, Hibernate (UTC), entity scan
    │   │   │   ├── KafkaConfig.kt            # Consumer/producer factories, listener container config
    │   │   │   ├── SchedulerConfig.kt        # @EnableScheduling + thread pools for jobs
    │   │   │   ├── SecurityConfig.kt         # REST + GraphQL auth (edge), method policies
    │   │   │   └── TemplatingConfig.kt       # Pebble/Handlebars in strict mode; renderers wired
    │   │   ├── ingress/                      # Ingress adapters only (validate → map → delegate)
    │   │   │   ├── rest/
    │   │   │   │   └── AlertController.kt    # POST /alerts/v1/send → uses models.requests + pipeline
    │   │   │   └── kafka/
    │   │   │       └── AlertsInboundConsumer.kt  # Consumes 'alerts-inbound'; commit after persist
    │   │   ├── admin/                         # Control plane (GraphQL), self-contained entrypoints
    │   │   │   ├── gql/
    │   │   │   │   ├── resolvers/            # GraphQL controllers
    │   │   │   │   │   ├── ChannelQueryResolver.kt
    │   │   │   │   │   ├── TemplateQueryResolver.kt
    │   │   │   │   │   ├── PreviewQueryResolver.kt
    │   │   │   │   │   ├── ChannelMutationResolver.kt
    │   │   │   │   │   └── TemplateMutationResolver.kt
    │   │   │   │   └── GraphQLConfig.kt      # Optional scalars, exception mapping, batching settings
    │   │   │   └── service/                  # Admin-only application services (no repo leakage from resolvers)
    │   │   │       ├── ChannelService.kt
    │   │   │       ├── TemplateService.kt
    │   │   │       └── PreviewService.kt
    │   │   ├── models/                        # **Standardized shapes**: requests, responses, errors
    │   │   │   ├── requests/
    │   │   │   │   ├── AlertSendRequestDto.kt   # title, severity, env, labels, payload, destinations…
    │   │   │   │   └── DestinationDto.kt        # { configRef, templateName, versionSelector }
    │   │   │   ├── responses/
    │   │   │   │   ├── SendResponseDto.kt       # { id, routedTo[], deduped }
    │   │   │   │   └── ErrorResponse.kt         # RFC7807-like (type, title, status, detail, traceId)
    │   │   │   └── errors/
    │   │   │       ├── ErrorCode.kt             # Stable client-facing error codes
    │   │   │       └── ProblemDetails.kt        # Internal problem mapped to ErrorResponse
    │   │   ├── enums/                           # Centralized enums used across layers
    │   │   │   ├── Severity.kt                  # CRITICAL/HIGH/MEDIUM/LOW/INFO
    │   │   │   ├── Environment.kt               # prod/stage/dev/qa (string-backed)
    │   │   │   ├── ChannelType.kt               # SLACK/PD/EMAIL/WEBHOOK
    │   │   │   └── DeliveryStatus.kt            # PENDING/SENT/FAILED/GAVE_UP
    │   │   ├── domain/                          # Pure business models (no frameworks)
    │   │   │   ├── DomainAlert.kt               # Canonical alert (post-normalization)
    │   │   │   ├── DeliveryIntent.kt            # One per destination (pre-persist)
    │   │   │   ├── TemplateHandle.kt            # { name, channelType }
    │   │   │   └── TemplateVersionRef.kt        # { name, channelType, version }
    │   │   ├── repository/                      # JPA entities + repos (H2 on PVC)
    │   │   │   ├── entity/
    │   │   │   │   ├── ChannelEntity.kt         # channel table
    │   │   │   │   ├── TemplateEntity.kt        # template table
    │   │   │   │   ├── AlertEventEntity.kt      # alert_event table (indexed for dedupe)
    │   │   │   │   └── AlertDeliveryEntity.kt   # alert_delivery table (status/next_attempt indexes)
    │   │   │   └── repo/
    │   │   │       ├── ChannelRepo.kt
    │   │   │       ├── TemplateRepo.kt
    │   │   │       ├── AlertEventRepo.kt
    │   │   │       └── AlertDeliveryRepo.kt
    │   │   ├── service/                         # Application core (pipeline & policies)
    │   │   │   ├── normalize/
    │   │   │   │   └── Normalizer.kt            # Canonicalize enums, compute/accept eventKey
    │   │   │   ├── idempotency/
    │   │   │   │   └── IdempotencyService.kt    # TTL window check via alert_event index
    │   │   │   ├── routing/
    │   │   │   │   ├── DestinationValidator.kt  # allowlists, enabled, paused_until checks
    │   │   │   │   └── TemplateResolver.kt      # {templateName, versionSelector} → concrete version
    │   │   │   ├── render/
    │   │   │   │   ├── RenderCoordinator.kt     # Chooses renderer per channel/format
    │   │   │   │   ├── JsonRenderer.kt          # Validates JSON payloads
    │   │   │   │   ├── HtmlRenderer.kt
    │   │   │   │   └── TextRenderer.kt
    │   │   │   ├── dispatch/
    │   │   │   │   ├── Dispatcher.kt            # Persist event+deliveries, then enqueue fanout
    │   │   │   │   └── InProcessDispatcher.kt   # Default impl using bounded executor queue
    │   │   │   ├── retry/
    │   │   │   │   └── BackoffPolicy.kt         # Exponential backoff + jitter helpers
    │   │   │   ├── health/
    │   │   │   │   └── CircuitBreakerService.kt # Track consecutive_failures → paused_until
    │   │   │   └── AlertPipeline.kt             # normalize → idempotency → route → render → persist → enqueue
    │   │   ├── workers/                         # Channel executors (Strategy pattern)
    │   │   │   ├── ChannelWorker.kt             # interface: supports(), send()
    │   │   │   ├── pagerduty/
    │   │   │   │   └── PagerDutyWorker.kt
    │   │   │   ├── slack/
    │   │   │   │   └── SlackWorker.kt
    │   │   │   ├── email/
    │   │   │   │   └── EmailWorker.kt
    │   │   │   └── webhook/
    │   │   │       └── WebhookWorker.kt
    │   │   ├── clients/                         # External clients (read **env var names** from channel.secret_env)
    │   │   │   ├── pd/PagerDutyClient.kt        # Reads routing key via env name; no secrets in DB
    │   │   │   ├── slack/SlackClient.kt         # Reads bot token via env name
    │   │   │   ├── smtp/SmtpClient.kt           # Reads SMTP creds via env names
    │   │   │   └── http/HttpClient.kt           # Signed POST helper (HMAC)
    │   │   ├── jobs/                            # Scheduled maintenance (uses repo indexes)
    │   │   │   ├── RedriverJob.kt               # Select by (status,next_attempt_at) and enqueue
    │   │   │   └── RetentionJob.kt              # Trim events/deliveries by policy
    │   │   ├── exception/                       # **Standardized REST errors** (lib-style)
    │   │   │   ├── GlobalExceptionHandler.kt    # @ControllerAdvice → ErrorResponse mapping
    │   │   │   ├── Exceptions.kt                # Domain exceptions (Validation, NotFound, RateLimit…)
    │   │   │   └── GraphQLExceptionAdapter.kt   # Maps domain errors to GraphQL error extensions
    │   │   └── util/
    │   │       ├── Hashing.kt                   # Stable fingerprint for eventKey when absent
    │   │       ├── Json.kt                      # JSON helpers (safe pretty-print)
    │   │       ├── IdGen.kt                     # Snowflake/simple sequence wrapper
    │   │       └── Signing.kt                   # HMAC utilities for webhooks
    │   └── resources
    │       ├── application.yaml                 # H2 on PVC; Hibernate validate; Kafka; retry/backoff; retention
    │       ├── graphql/
    │       │   └── schema.graphqls              # **Standard Spring GraphQL location**
    │       ├── templates/                       # Sample preview bodies (non-secret, local testing only)
    │       └── db/
    │           └── schema.sql                   # **Authoritative DDL** for 4 tables + indexes (H2/Postgres-compatible)
    └── test
        ├── kotlin/ca/bell/wireless/alerting
        │   ├── ingress/rest/AlertControllerTest.kt
        │   ├── service/AlertPipelineTest.kt
        │   ├── service/idempotency/IdempotencyServiceTest.kt
        │   ├── workers/slack/SlackWorkerTest.kt
        │   └── admin/gql/SchemaSmokeTest.kt
        └── resources/
```

---

## 1. Overview

The `alerting-service` is a **source-agnostic alerting platform** that:

* Accepts alerts through **REST API** and **Kafka**.
* Deduplicates events using an **idempotency key** (`eventKey`).
* Persists the alert event and its delivery intents in **H2 (on PVC)**.
* Fans out asynchronously to **Slack**, **PagerDuty**, **Email**, and **Webhooks**.
* Provides a **GraphQL admin plane** to manage channels and templates.
* Guarantees **exactly-once effect**, **eventual consistency**, and **fast acknowledgment**.

---

## 2. Project Structure (authoritative)

*(Structure already defined above — assumed in repo.)*

Each package is a self-contained concern. The developer should never cross-reference horizontally between layers (e.g., no `repository` call from `ingress` directly).

---

## 3. Core Flow (Step-by-Step)

### 3.1 Ingress (Entry Layer)

Handles all inputs and converts them to an internal canonical form (`DomainAlert`).

#### `AlertController` (REST)

* Endpoint: `POST /alerts/v1/send`
* Validates `AlertSendRequestDto`
* Logs `traceId`
* Calls:

  ```kotlin
  alertPipeline.process(request)
  ```
* Returns `SendResponseDto(id, routedTo, deduped)`.

#### `AlertsInboundConsumer` (Kafka)

* Listens to topic `alerts-inbound`
* Consumes JSON payloads identical to REST body
* Delegates to `AlertPipeline.process()`
* Commits offset **after** successful persistence

**Purpose:** REST provides synchronous intake, Kafka supports async bulk ingestion.

---

### 3.2 Pipeline (Application Core)

The **AlertPipeline** orchestrates the full lifecycle.

```
[normalize] → [idempotency] → [validate] → [resolve template] → [render] → [persist] → [enqueue]
```

#### `Normalizer`

* Converts enums (Severity, Environment, etc.)
* Ensures `eventKey` is available:

  * Use provided value if present
  * Else compute deterministic hash using `Hashing.kt`:

    ```kotlin
    Hashing.stableFingerprint("${title}:${domain}:${labels}")
    ```
* Produces `DomainAlert`.

#### `IdempotencyService`

* Looks up recent `alert_event` by `event_key` within TTL.

  ```sql
  SELECT id FROM alert_event
  WHERE event_key=:key AND created_at > NOW() - INTERVAL :ttl SECOND;
  ```
* If found → dedupe hit → return `deduped=true`.
* Else → continue.

#### `DestinationValidator`

* Loads `channel` config by `ref`.
* Ensures:

  * Channel exists and `enabled == true`
  * `paused_until` is null or expired
* If invalid → throw `ValidationException`.

#### `TemplateResolver`

* Resolves template per destination:

  * `"latest"` → max(version)
  * `"2"` → exact match
* Returns `TemplateVersionRef(name, channelType, version)`.

#### `RenderCoordinator`

* Chooses renderer based on template format.
* Supported: JSON, HTML, TEXT.
* Uses Pebble/Handlebars strict mode (missing var = exception).
* Returns map:

  ```kotlin
  Map<DestinationRef, RenderedBody>
  ```

#### `Dispatcher`

* Begins DB transaction.

  1. Inserts into `alert_event`.
  2. Inserts one row per destination into `alert_delivery`.
* Commits transaction.
* Queues all delivery IDs into `InProcessDispatcher.enqueue()`.
* Returns persisted `eventId` and `routedRefs`.

#### `AlertPipeline.process()`

```kotlin
val normalized = normalizer.toDomain(request)
if (idempotency.isDuplicate(normalized)) {
    return SendResponseDto(idempotency.lastId(), emptyList(), true)
}
val validated = destinationValidator.validate(normalized)
val resolved = templateResolver.resolve(validated)
val rendered = renderer.renderAll(resolved)
val persisted = dispatcher.persistEventAndDeliveries(normalized, rendered)
dispatcher.enqueue(persisted)
return SendResponseDto(persisted.eventId, persisted.routedRefs, false)
```

---

## 4. Worker Layer

Each delivery record corresponds to one worker job.
Workers run asynchronously inside a bounded thread pool managed by `InProcessDispatcher`.

### `ChannelWorker` (interface)

```kotlin
interface ChannelWorker {
    fun supports(channel: ChannelType): Boolean
    fun send(delivery: AlertDeliveryEntity, renderedBody: RenderedBody): WorkerResult
}
```

### Common Worker Flow

1. Resolve secrets from environment variables:

   ```kotlin
   val token = System.getenv(secretEnv["tokenEnv"])
   ```
2. Send to provider.
3. Update `alert_delivery` row:

   * `status = SENT | FAILED`
   * `attempts += 1`
   * `external_id` (if available)
   * `next_attempt_at = backoff.nextDelay(attempts)`
4. If send failed → backoff + retry via `RedriverJob`.

### Example: SlackWorker

* Reads token via `SlackClient`.
* Posts to `chat.postMessage` or webhook.
* Parses Slack `ts` as `external_id`.
* Updates DB on success/failure.

### Example: PagerDutyWorker

* Uses `PagerDutyClient` and PD Events v2 API.
* Dedup key = `eventKey` (exactly-once per alert).

---

## 5. Persistence & Entities

### 5.1 Tables (from `resources/db/schema.sql`)

**`channel`**

* Connector metadata + state.
* `secret_env` JSON stores only **env var names**.

**`template`**

* Versioned templates by `(name, channel, version)`.

**`alert_event`**

* Source events (dedupe anchor).
* Indexed by `(event_key, created_at)`.

**`alert_delivery`**

* Per-destination delivery records.
* Indexed by `(status, next_attempt_at)`.

### 5.2 Entity Classes

Each maps 1:1 to table with Spring JPA annotations.

Example:

```kotlin
@Entity
@Table(name = "alert_event")
data class AlertEventEntity(
  @Id @GeneratedValue var id: Long? = null,
  var eventKey: String,
  var title: String,
  var severity: String,
  var environment: String,
  var domain: String,
  var labels: String?,
  var payload: String?,
  var dedupeTtlSeconds: Int,
  var createdAt: Instant = Instant.now()
)
```

Repositories (`AlertEventRepo`, `AlertDeliveryRepo`, etc.) expose finder methods.

---

## 6. GraphQL Control Plane

### Purpose

Manage configurations (channels, templates) via a **single strongly-typed endpoint**.

### Components

| Component                  | Role                                     |
| -------------------------- | ---------------------------------------- |
| `ChannelQueryResolver`     | Fetch all or specific channels           |
| `TemplateQueryResolver`    | List templates and versions              |
| `PreviewQueryResolver`     | Render preview with sample event         |
| `ChannelMutationResolver`  | Upsert / Pause channel                   |
| `TemplateMutationResolver` | Add template / new version               |
| Services                   | Contain actual logic; resolvers delegate |

### Example: `upsertChannel`

```graphql
mutation {
  upsertChannel(input: {
    ref: "slack_ops",
    type: "SLACK",
    secretEnv: "{\"tokenEnv\":\"SLACK_OPS_TOKEN\"}"
  }) {
    ref
    enabled
  }
}
```

---

## 7. Error & Exception Handling

### REST (Global)

`GlobalExceptionHandler` catches:

* `ValidationException` → 400
* `EntityNotFoundException` → 404
* Generic → 500

Produces uniform response:

```json
{
  "type": "https://alerting.bell.ca/errors/validation",
  "title": "Invalid request",
  "status": 400,
  "detail": "Field 'severity' missing",
  "traceId": "abc123"
}
```

### GraphQL

Handled by `GraphQLExceptionAdapter` → adds `extensions.code` for clients.

---

## 8. Concurrency Model

### Ingress

* REST → multiple threads (Tomcat). Stateless controller.
* Kafka → `concurrency=N` listener threads; each consumes a partition.

### Pipeline

* All services stateless and thread-safe.
* DB write per alert = one transaction (atomic).

### Fanout

* `InProcessDispatcher` uses:

  ```kotlin
  Executors.newFixedThreadPool(cores * 2)
  ```
* `LinkedBlockingQueue` bounded by 10,000 tasks.
* Each worker handles its own retry logic, so no shared mutable state.

### Safety

* Idempotency ensures duplicate messages (Kafka re-delivery or retries) don’t produce double sends.
* Redriver uses CAS update to avoid double claiming (`WHERE status IN ('PENDING','FAILED')`).

---

## 9. Resiliency & Fault Tolerance

| Mechanism             | Purpose                       | Implementation                               |
| --------------------- | ----------------------------- | -------------------------------------------- |
| **Backpressure**      | Prevent overload              | Bounded worker queue; backoff + retry        |
| **Circuit Breaker**   | Pause failing connectors      | `paused_until` + `consecutive_failures`      |
| **Rate Limiter**      | Avoid API throttling          | Token bucket per channel                     |
| **Retry Policy**      | Ensure eventual success       | `BackoffPolicy` (exp + jitter)               |
| **Crash Safety**      | Resume after crash            | `RedriverJob` re-enqueues pending deliveries |
| **Partial Isolation** | Contain failures per provider | Separate executors by channel type           |

---

## 10. Consistency & Reliability

| Level      | Model                | Guarantee                                             |
| ---------- | -------------------- | ----------------------------------------------------- |
| In-DB      | Strong consistency   | `alert_event` + `alert_delivery` persisted atomically |
| Ingress→DB | Exactly-once effect  | Commit offset only after commit                       |
| External   | Eventual consistency | Retry + idempotent API integration                    |

**Example:**

* REST returns success → event persisted.
* Worker fails → `alert_delivery.status=FAILED`.
* Redriver picks it up later → success → `SENT`.
* No duplicates because same `deliveryId` is reused.

---

## 11. Latency Optimization

| Step                       | Description             | Target Duration   |
| -------------------------- | ----------------------- | ----------------- |
| Normalize & dedupe lookup  | In-memory + indexed SQL | 1–3 ms            |
| Persist event + deliveries | Single transaction      | 10–15 ms          |
| Enqueue to worker pool     | Non-blocking            | < 1 ms            |
| **Total REST response**    | Persisted + ack         | **< 50 ms (avg)** |
| Deduped request            | Early exit              | **~2 ms**         |

User never waits for external send; acknowledgment happens post-persistence.

---

## 12. Jobs (Scheduled Maintenance)

### `RedriverJob`

* Runs every 1 minute.
* Query:

  ```sql
  SELECT * FROM alert_delivery
  WHERE status IN ('FAILED','PENDING')
  AND next_attempt_at <= now();
  ```
* Resubmits each eligible delivery to the worker queue.

### `RetentionJob`

* Daily cleanup:

  * Delete `alert_event` older than 14d.
  * Delete deliveries (SENT>7d, FAILED>30d).
* Paginated deletes (10k batch) to avoid locks.

---

## 13. Observability

### Metrics (Micrometer)

| Metric                    | Description               |
| ------------------------- | ------------------------- |
| `alerts_ingested_total`   | Count of alerts accepted  |
| `alerts_deduped_total`    | Dedupe hits               |
| `delivery_attempts_total` | Per-channel send attempts |
| `delivery_failures_total` | Per-channel failures      |
| `circuit_open_total`      | Channels paused           |

### Logs

* Structured JSON:
  `eventKey`, `eventId`, `deliveryId`, `channel`, `status`, `attempts`, `error`.

### Traces

* `AlertPipeline` → parent span
* Worker → child span (each delivery send)

---

## 14. Configuration Parameters

```yaml
alerting:
  retry:
    base-seconds: 5
    max-seconds: 300
    max-attempts: 6
  breaker:
    failure-threshold: 8
    pause-minutes: 15
  retention:
    events-days: 14
    deliveries-sent-days: 7
    deliveries-failed-days: 30
  dispatch:
    queue-capacity: 10000
    per-channel-executors: true
```

---

## 15. Testing Strategy

| Layer      | Framework         | Example                           |
| ---------- | ----------------- | --------------------------------- |
| Controller | `@WebMvcTest`     | Validate REST schema              |
| Kafka      | `@EmbeddedKafka`  | Ensure commit after persist       |
| Pipeline   | JUnit5 + Mockito  | `AlertPipelineTest`               |
| Workers    | Mock API          | `SlackWorkerTest`, `PDWorkerTest` |
| GraphQL    | `@SpringBootTest` | Query & mutation tests            |

Integration tests simulate dedupe, crash, retry, and breaker recovery.

---

## 17. Guarantees Summary

| Concern                     | Guarantee    | Mechanism                               |
| --------------------------- | ------------ | --------------------------------------- |
| Fast producer response      | ✅ <50 ms avg | Persist → Ack → Async delivery          |
| No duplicate sends          | ✅            | Dedupe window + idempotent workers      |
| Eventual delivery           | ✅            | Backoff + Redriver                      |
| Isolation per connector     | ✅            | Circuit breaker + per-channel executors |
| Strong internal consistency | ✅            | Transactional persistence               |
| Secret isolation            | ✅            | Env-based credential resolution         |

