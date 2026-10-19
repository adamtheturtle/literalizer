import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("[-42, 0, 42, -1.25, 0.0, 1.25]")
