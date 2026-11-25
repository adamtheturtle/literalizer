import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val my_null: JsonElement = Json.parseToJsonElement("null")
val regular_null: JsonElement = Json.parseToJsonElement("null")
consume(value = my_null)
consume(value = regular_null)
