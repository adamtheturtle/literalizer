import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"test\": [5, [\"compile\", \"test\"]], \"package\": [7, [\"link\", \"test\"]]}")
