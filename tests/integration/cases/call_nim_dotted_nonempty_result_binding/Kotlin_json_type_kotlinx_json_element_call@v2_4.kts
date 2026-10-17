import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
class _ThingType { fun go(value: Any? = null): Any? = listOf<Any?>(value) }
val thing = _ThingType()
val my_data = thing.go(value = Json.parseToJsonElement("[1]"))
