import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume(value: Any? = null): Any? = null
val shared: JsonElement = Json.parseToJsonElement("[1, 2]")
consume(value = Json.parseToJsonElement("{\"field\": {\"\$ref\": \"shared\"}, \"nested\": [{\"\$ref\": \"shared\"}, {}]}"))
