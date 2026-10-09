import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume(value: Any? = null): Any? = null
val item: JsonElement = Json.parseToJsonElement("\"s\"")
consume(value = item)
