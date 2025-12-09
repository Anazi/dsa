
# NasNotifyBridge — Low-Level Design

## Build & runtime

* **Build**: Maven (`pom.xml`)
* **Lang**: Kotlin 1.9+
* **Spring Boot 3**: Web, Validation, Actuator (health only if you want), Scheduling, Spring Data JPA, Spring for Apache Kafka, Micrometer
* **DB**: H2 (file on PVC), Postgres-compatible DDL
* **HTTP**: WebClient

---

## Project layout (authoritative)

```
nas-notify-bridge/
├── pom.xml
└── src
    ├── main
    │   ├── kotlin/com/acme/nasbridge
    │   │   ├── App.kt                          # @SpringBootApplication
    │   │   ├── config/
    │   │   │   ├── AppConfig.kt               # @ConfigurationProperties(prefix="bridge") + beans
    │   │   │   ├── KafkaConfig.kt             # consumer factory, listener container props
    │   │   │   ├── WebClientConfig.kt         # NC WebClient + auth filter
    │   │   │   ├── PersistenceConfig.kt       # JPA + Clock
    │   │   │   └── MappingConfig.kt           # mappings.json loader + (optional) JSON Schema
    │   │   ├── enums/
    │   │   │   ├── EventStatus.kt             # PENDING, SENT, FAILED, GAVE_UP
    │   │   │   ├── Severity.kt                # CRITICAL, HIGH, MEDIUM, LOW, INFO
    │   │   │   ├── Environment.kt             # prod, stage, dev, qa
    │   │   │   └── ChannelType.kt             # SLACK, PD, EMAIL, WEBHOOK (if needed for logs)
    │   │   ├── mapping/
    │   │   │   ├── MappingModel.kt            # DTOs for mappings.json
    │   │   │   ├── MappingEvaluator.kt        # first-match-wins evaluator
    │   │   │   └── MappingSchema.json         # optional schema for validation
    │   │   ├── clients/
    │   │   │   ├── KafkaConsumerClient.kt     # abstraction + NAS consumer impl
    │   │   │   └── NcClient.kt                # REST client for /alerts/v1/send
    │   │   ├── kafka/
    │   │   │   ├── NasMessage.kt              # NAS→Bridge DTO
    │   │   │   └── NasKafkaListener.kt        # @KafkaListener (uses KafkaConsumerClient)
    │   │   ├── repository/
    │   │   │   ├── entity/BridgeDeliveryEntity.kt
    │   │   │   └── repo/BridgeDelivery.kt
    │   │   ├── service/
    │   │   │   ├── Normalizer.kt
    │   │   │   ├── Router.kt
    │   │   │   ├── ResiliencyQueue.kt
    │   │   │   ├── RetryScheduler.kt
    │   │   │   └── CleanupScheduler.kt
    │   │   └── util/
    │   │       ├── Backoff.kt
    │   │       ├── EventKey.kt
    │   │       └── Json.kt
    │   └── resources/
    │       ├── application.yml
    │       ├── db/schema.sql                  # authoritative DDL
    │       └── config/mappings.json           # mounted path in containers
    └── test/…                                 # unit & slice tests
```

> Notes:
>
> * `/clients` now holds **both** `NcClient` and the **KafkaConsumerClient** abstraction (plus its NAS implementation).
> * No `ingress` package.
> * `HealthController` removed (Spring Actuator endpoints optional via config).

---

## Enums

`enums/EventStatus.kt`

```kotlin
package com.acme.nasbridge.enums
enum class EventStatus { PENDING, SENT, FAILED, GAVE_UP }
```

`enums/Severity.kt`

```kotlin
package com.acme.nasbridge.enums
enum class Severity { CRITICAL, HIGH, MEDIUM, LOW, INFO }
```

`enums/Environment.kt`

```kotlin
package com.acme.nasbridge.enums
enum class Environment { prod, stage, dev, qa }
```

`enums/ChannelType.kt` *(optional, useful for logs/metrics)*

```kotlin
package com.acme.nasbridge.enums
enum class ChannelType { SLACK, PD, EMAIL, WEBHOOK }
```

---

## AppConfig (replaces AppProps)

`config/AppConfig.kt`

```kotlin
package com.acme.nasbridge.config

import org.springframework.boot.context.properties.ConfigurationProperties

@ConfigurationProperties(prefix = "bridge")
data class AppConfig(
  val kafka: Kafka = Kafka(),
  val nc: Nc = Nc(),
  val retry: Retry = Retry(),
  val cleanup: Cleanup = Cleanup(),
  val config: Config = Config()
) {
  data class Kafka(
    var bootstrap: String = "",
    var topic: String = "nas.actions.alerts",
    var groupId: String = "nas-notify-bridge",
    var listenerConcurrency: Int = 4,
    var filterEnabled: Boolean = true,
    var filterIncludeDomain: String = "CoreRules"
  )
  data class Nc(
    var baseUrl: String = "",
    var timeoutMs: Long = 2000,
    var authMode: String = "mtls" // or "hmac"
  )
  data class Retry(
    var enabled: Boolean = true,
    var scheduleFixedDelayMs: Long = 10_000,
    var workers: Int = 8,
    var claimBatchSize: Int = 200,
    var baseMs: Long = 5_000,
    var maxMs: Long = 300_000,
    var maxAttempts: Int = 6,
    var leaseMinutes: Long = 5
  )
  data class Cleanup(
    var enabled: Boolean = true,
    var cron: String = "0 0 * * * *",
    var workers: Int = 2,
    var batchSize: Int = 1000,
    var retentionSentDays: Long = 7,
    var retentionFailedDays: Long = 30
  )
  data class Config(
    var dir: String = "/etc/nas-bridge/config",
    var mappingsJson: String = "/etc/nas-bridge/config/mappings.json"
  )
}
```

Register in `App.kt`:

```kotlin
@SpringBootApplication
@EnableConfigurationProperties(AppConfig::class)
class App
fun main(args: Array<String>) = runApplication<App>(*args)
```

---

## Clients

### KafkaConsumerClient (plus NAS impl)

`clients/KafkaConsumerClient.kt`

```kotlin
package com.acme.nasbridge.clients

interface KafkaConsumerClient<T> {
  fun handle(message: T)
}
```

`kafka/NasMessage.kt` (unchanged DTO)

`kafka/NasKafkaListener.kt` (delegates to the client)

```kotlin
package com.acme.nasbridge.kafka

@Component
class NasKafkaListener(
  private val app: AppConfig,
  private val nasConsumer: KafkaConsumerClient<NasMessage>
) {
  @KafkaListener(
    topics = ["\${bridge.kafka.topic}"],
    groupId = "\${bridge.kafka.groupId}",
    concurrency = "\${bridge.kafka.listener-concurrency}" // kebab-case binds to listenerConcurrency
  )
  fun onMessage(record: ConsumerRecord<String, String>) {
    val msg = mapper.readValue(record.value(), NasMessage::class.java)
    if (app.kafka.filterEnabled && msg.domain != app.kafka.filterIncludeDomain) return
    nasConsumer.handle(msg)
  }
}
```

`clients/NasKafkaConsumer.kt` (implementation of the interface)

```kotlin
package com.acme.nasbridge.clients

@Component
class NasKafkaConsumer(
  private val normalizer: Normalizer,
  private val router: Router,
  private val queue: ResiliencyQueue
) : KafkaConsumerClient<NasMessage> {

  override fun handle(message: NasMessage) {
    val normalized = normalizer.normalize(message)
    val routes = router.route(normalized)
    queue.enqueueAndTrySend(normalized, routes) // persist, attempt once, update DB, move on
  }
}
```

### NcClient (moved to /clients)

`clients/NcClient.kt`

```kotlin
package com.acme.nasbridge.clients

@Component
class NcClient(private val webClient: WebClient, private val cfg: AppConfig) {
  sealed interface Result {
    data class Ok(val body: Map<String, Any?>) : Result
    data class Retryable(val msg: String) : Result
    data class NonRetryable(val msg: String) : Result
  }

  fun send(row: BridgeDeliveryEntity): Result = runCatching {
    val req = NcRequest(/* build from row */)
    val resp = webClient.post()
      .uri("${cfg.nc.baseUrl}/alerts/v1/send")
      .bodyValue(req)
      .retrieve()
      .toEntity(object : ParameterizedTypeReference<Map<String, Any?>>() {})
      .block(Duration.ofMillis(cfg.nc.timeoutMs))
    Result.Ok(resp?.body ?: emptyMap())
  }.getOrElse { e ->
    when (e) {
      is WebClientResponseException.BadRequest,
      is WebClientResponseException.UnprocessableEntity,
      is WebClientResponseException.NotFound -> Result.NonRetryable(e.message ?: "4xx")
      is WebClientResponseException -> Result.Retryable("HTTP ${e.statusCode.value()}")
      is IOException, is TimeoutException -> Result.Retryable(e.message ?: "io/timeout")
      else -> Result.Retryable(e.message ?: "unknown")
    }
  }
}
```

---

## Entity updates (use your enums)

`repository/entity/BridgeDeliveryEntity.kt`

```kotlin
@Entity @Table(name = "bridge_delivery")
class BridgeDeliveryEntity(
  @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
  var id: Long? = null,
  var nasEventId: String,
  var eventKey: String,
  var actionType: String,
  @Enumerated(EnumType.STRING) var severity: Severity,
  @Enumerated(EnumType.STRING) var environment: Environment,
  var domain: String = "CoreRules",
  @Lob var labelsJson: String? = null,
  @Lob var payloadJson: String? = null,
  @Lob var destinationsJson: String,

  @Enumerated(EnumType.STRING)
  var status: EventStatus = EventStatus.PENDING,

  var attempts: Int = 0,
  var nextAttemptAt: Instant? = null,
  @Lob var lastError: String? = null,
  @Lob var externalResp: String? = null,
  var claimedBy: String? = null,
  var claimedAt: Instant? = null,
  var createdAt: Instant = Instant.now(),
  var updatedAt: Instant = Instant.now()
) {
  @PreUpdate fun touch() { updatedAt = Instant.now() }
}
```

---

## Services (unchanged logic, updated imports)

* **Normalizer.kt**: produces domain DTO using `Severity`/`Environment` enums.
* **Router.kt**: uses `MappingEvaluator` and returns route refs.
* **ResiliencyQueue.kt**: persists, one-shot send via `NcClient`, transitions `EventStatus`.
* **RetryScheduler.kt / CleanupScheduler.kt**: as in previous LLD; thread pools sized from `AppConfig.retry.workers` / `AppConfig.cleanup.workers`.

---

## DDL (unchanged, enum columns now strings)

`resources/db/schema.sql`

```sql
CREATE TABLE IF NOT EXISTS bridge_delivery (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  nas_event_id      VARCHAR(128) NOT NULL,
  event_key         VARCHAR(256) NOT NULL,
  action_type       VARCHAR(64)  NOT NULL,
  severity          VARCHAR(32)  NOT NULL,
  environment       VARCHAR(32)  NOT NULL,
  domain            VARCHAR(64)  NOT NULL,
  labels_json       CLOB NULL,
  payload_json      CLOB NULL,
  destinations_json CLOB NOT NULL,
  status            VARCHAR(16)  NOT NULL,
  attempts          INT          NOT NULL DEFAULT 0,
  next_attempt_at   TIMESTAMP    NULL,
  last_error        CLOB NULL,
  external_resp     CLOB NULL,
  claimed_by        VARCHAR(64)  NULL,
  claimed_at        TIMESTAMP    NULL,
  created_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_bridge_status_due ON bridge_delivery (status, next_attempt_at);
CREATE INDEX IF NOT EXISTS ix_bridge_eventkey   ON bridge_delivery (event_key, created_at);
CREATE INDEX IF NOT EXISTS ix_bridge_created_at ON bridge_delivery (created_at);
```

---

## Kafka & WebClient configs (point to AppConfig)

* `KafkaConfig.kt`: set concurrency from `AppConfig.kafka.listenerConcurrency`.
* `WebClientConfig.kt`: base URL/timeouts from `AppConfig.nc`, auth from `authMode`.

---

## Tests to add/keep

* `MappingEvaluatorTest`, `NormalizerTest`
* `ResiliencyQueueTest` (status transitions using `EventStatus`)
* `RetrySchedulerTest` (lease + backoff)
* `NcClientTest` (2xx/4xx/5xx mapping)
* `NasKafkaListenerSlice` (filter passes/drops)

