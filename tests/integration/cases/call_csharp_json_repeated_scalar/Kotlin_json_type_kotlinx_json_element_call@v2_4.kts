import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val shared: JsonElement = Json.parseToJsonElement("42")
consume(value = Json.parseToJsonElement("[{\"\$ref\": \"shared\"}, {\"\$ref\": \"shared\"}]"))
