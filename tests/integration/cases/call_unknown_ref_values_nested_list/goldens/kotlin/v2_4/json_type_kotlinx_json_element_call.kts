import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun process(data: Any? = null): Any? = listOf<Any?>(data)
val unknown_value: JsonElement = Json.parseToJsonElement("[]")
process(data = Json.parseToJsonElement("[{\"\$ref\": \"unknown_value\"}]"))
