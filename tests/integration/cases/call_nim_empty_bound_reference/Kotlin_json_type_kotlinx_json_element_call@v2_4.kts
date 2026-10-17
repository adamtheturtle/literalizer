import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun make_widget(value: Any? = null): Any? = listOf<Any?>(value)
val items: JsonElement = Json.parseToJsonElement("[]")
make_widget(value = items)
