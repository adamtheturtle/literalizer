import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun process(value: Any? = null): Any? = listOf<Any?>(value)
process(value = Json.parseToJsonElement("\"hello\""))
process(value = Json.parseToJsonElement("42"))
process(value = Json.parseToJsonElement("true"))
