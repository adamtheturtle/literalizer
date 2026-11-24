import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
var shared: JsonElement = Json.parseToJsonElement("42")
var my_data: JsonElement = Json.parseToJsonElement("[42, 42]")
