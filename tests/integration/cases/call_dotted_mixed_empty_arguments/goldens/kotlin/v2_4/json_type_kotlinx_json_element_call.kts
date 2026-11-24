import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
class _ThingType { fun go(before: Any? = null, populated: Any? = null, after: Any? = null): Any? = listOf<Any?>(before, populated, after) }
val thing = _ThingType()
thing.go(before = Json.parseToJsonElement("[]"), populated = Json.parseToJsonElement("[1]"), after = Json.parseToJsonElement("[]"))
thing.go(before = Json.parseToJsonElement("[\"text\"]"), populated = Json.parseToJsonElement("[2]"), after = Json.parseToJsonElement("[]"))
thing.go(before = Json.parseToJsonElement("[]"), populated = Json.parseToJsonElement("[\"text\"]"), after = Json.parseToJsonElement("[]"))
thing.go(before = Json.parseToJsonElement("[\"text\"]"), populated = Json.parseToJsonElement("[2]"), after = Json.parseToJsonElement("[3]"))
