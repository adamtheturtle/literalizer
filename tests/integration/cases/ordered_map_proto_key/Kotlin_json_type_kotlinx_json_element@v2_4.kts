import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"__proto__\": {\"x\": 1}, \"ordinary\": 2}")
