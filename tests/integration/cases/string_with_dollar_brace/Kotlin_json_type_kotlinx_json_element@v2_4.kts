import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("[\"prefix \${HOME} suffix\", \"\${interpolated}\"]")
