import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val shared: JsonElement = Json.parseToJsonElement("null")
consume(value = Json.parseToJsonElement("{\"left\": {\"\$ref\": \"shared\"}, \"nested\": [{\"\$ref\": \"shared\"}]}"))
