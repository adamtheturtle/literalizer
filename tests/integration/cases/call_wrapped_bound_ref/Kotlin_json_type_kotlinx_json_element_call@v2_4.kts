import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun make_widget(value: Any? = null): Any? = listOf<Any?>(value)
val value: JsonElement = Json.parseToJsonElement("1")
make_widget(value = value)
