import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("\"\\nroot first line\\n  indented\\n\\nroot last line\\n\"")
