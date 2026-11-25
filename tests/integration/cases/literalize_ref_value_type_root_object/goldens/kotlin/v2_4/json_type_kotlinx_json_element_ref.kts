import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val shared: JsonElement = Json.parseToJsonElement("{\"field\": [1, 2]}")
val my_data: JsonElement = Json.parseToJsonElement("{\"field\": [1, 2]}")
