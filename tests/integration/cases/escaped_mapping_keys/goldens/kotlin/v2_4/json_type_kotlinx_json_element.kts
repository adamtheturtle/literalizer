import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"quote\\\"backslash\\\\\": 1, \"line\\nbreak\": 2, \"\$(literal)\${text}\": 3, \"RStr prefix\": 4}")
