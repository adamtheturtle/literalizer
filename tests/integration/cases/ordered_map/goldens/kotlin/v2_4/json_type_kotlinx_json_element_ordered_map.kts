import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"name\": \"Alice\", \"age\": 30, \"active\": true}")
