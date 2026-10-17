import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
fun make_widget(before: Any? = null, populated: Any? = null, after: Any? = null): Any? = listOf<Any?>(before, populated, after)
make_widget(before = Json.parseToJsonElement("[]"), populated = Json.parseToJsonElement("[1]"), after = Json.parseToJsonElement("[]"))
make_widget(before = Json.parseToJsonElement("[\"text\"]"), populated = Json.parseToJsonElement("[2]"), after = Json.parseToJsonElement("[]"))
make_widget(before = Json.parseToJsonElement("[]"), populated = Json.parseToJsonElement("[\"text\"]"), after = Json.parseToJsonElement("[]"))
make_widget(before = Json.parseToJsonElement("[\"text\"]"), populated = Json.parseToJsonElement("[2]"), after = Json.parseToJsonElement("[3]"))
