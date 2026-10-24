import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("[[\"\\nfirst line\\n  indented\\n\\nlast line\\n\"]]")
