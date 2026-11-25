import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun process(data: Any? = null): Any? = listOf<Any?>(data)
val untypedValue: JsonElement = Json.parseToJsonElement("[]")
process(data = Json.parseToJsonElement("[{\"@reference\": \"untyped_value\"}, {\"@reference\": \"untyped_value\"}]"))
