import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun make_widget(value: Any? = null): Any? = listOf<Any?>(value)
val my_data = make_widget(value = Json.parseToJsonElement("[]"))
