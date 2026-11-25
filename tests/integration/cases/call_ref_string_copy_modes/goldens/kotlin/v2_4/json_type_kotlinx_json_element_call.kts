import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val item: JsonElement = Json.parseToJsonElement("\"s\"")
consume(value = item)
