import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val shared: JsonElement = Json.parseToJsonElement("[1, 2]")
consume(value = Json.parseToJsonElement("[{\"\$ref\": \"shared\"}, 42]"))
