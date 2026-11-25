import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"outer\": [[\"nested first line\\n  indented\\n\\nnested last line\\n\"]]}")
