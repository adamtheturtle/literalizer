import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"times\": [\"09:30:00\", \"17:45:00\", \"23:59:59\"]}")
