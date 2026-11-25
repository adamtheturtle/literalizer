import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("[\"price \$10\", \"\$HOME\"]")
