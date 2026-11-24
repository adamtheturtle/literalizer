import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun consume_widget(arg_value: Any? = null): Any? = listOf<Any?>(arg_value)
var my_data: JsonElement = Json.parseToJsonElement("{\"a\": 0}")
consume_widget(arg_value = my_data)
my_data = Json.parseToJsonElement("{\"a\": 1}")
consume_widget(arg_value = my_data)
