import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val shared: JsonElement = Json.parseToJsonElement("42")
val my_data: JsonElement = Json.parseToJsonElement("{\"refs\": [42, 42], \"quoted\": \"#{shared}\"}")
