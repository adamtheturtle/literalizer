import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume_widget(arg_value: Any? = null): Any? = listOf<Any?>(arg_value)
val item: JsonElement = Json.parseToJsonElement("null")
var my_data: JsonElement = Json.parseToJsonElement("null")
consume_widget(arg_value = my_data)
my_data = Json.parseToJsonElement("null")
consume_widget(arg_value = my_data)
