import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"within_i32\": \"2024-01-15T12:00:00\", \"beyond_i32\": \"2099-06-15T08:30:00\"}")
