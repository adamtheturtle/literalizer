import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun process(value: Any? = null): Any? = listOf<Any?>(value)
fun emit(_call: Any? = null, _zip: Any? = null): Any? = listOf<Any?>(_call, _zip)
emit(process(value = Json.parseToJsonElement("1")), Json.parseToJsonElement("\"2024-01-15T12:00:00\""))
