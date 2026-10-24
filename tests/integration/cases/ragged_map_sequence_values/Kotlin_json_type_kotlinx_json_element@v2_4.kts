import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"a\": [{\"item\": [1]}], \"b\": [{\"item\": [2, 3]}]}")
