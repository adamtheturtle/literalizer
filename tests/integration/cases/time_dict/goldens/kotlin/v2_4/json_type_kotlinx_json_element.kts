import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"morning\": \"09:30:00\", \"afternoon\": \"14:15:00\", \"evening\": \"23:59:59\"}")
