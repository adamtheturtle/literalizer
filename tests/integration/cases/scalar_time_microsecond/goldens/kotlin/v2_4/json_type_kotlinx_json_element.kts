import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"exact_millisecond\": \"09:30:15.123000\", \"sub_millisecond\": \"09:30:15.123456\"}")
