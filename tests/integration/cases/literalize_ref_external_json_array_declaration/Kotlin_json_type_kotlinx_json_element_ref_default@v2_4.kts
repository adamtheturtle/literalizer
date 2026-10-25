import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume_widget(arg_value: Any? = null): Any? = listOf<Any?>(arg_value)
val shared: JsonElement = Json.parseToJsonElement("[1, 2]")
val my_data: JsonElement = Json.parseToJsonElement("[1, 2]")
consume_widget(arg_value = my_data)
