import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun process(value: Any? = null): Any? = null
val arena: JsonElement = Json.parseToJsonElement("{\"a\": 1}")
val ZVal: JsonElement = Json.parseToJsonElement("{\"a\": 1}")
val ZKV: JsonElement = Json.parseToJsonElement("{\"a\": 1}")
process(value = arena)
process(value = ZVal)
process(value = ZKV)
