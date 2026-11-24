import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"cr\": \"a\\rb\", \"crlf\": \"a\\r\\nb\", \"lf\": \"a\\nb\"}")
