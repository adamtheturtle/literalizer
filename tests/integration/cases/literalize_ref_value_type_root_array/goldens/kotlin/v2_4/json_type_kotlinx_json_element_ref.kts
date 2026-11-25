import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val shared: JsonElement = Json.parseToJsonElement("[1, 2]")
val my_data: JsonElement = Json.parseToJsonElement("[1, 2]")
