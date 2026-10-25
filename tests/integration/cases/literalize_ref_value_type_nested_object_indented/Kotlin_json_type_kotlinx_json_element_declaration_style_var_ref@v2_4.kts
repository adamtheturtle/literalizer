import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
        var shared: JsonElement = Json.parseToJsonElement("[1, 2]")
        var my_data: JsonElement = Json.parseToJsonElement("{\"field\": {\"nested\": [1, 2]}, \"text\": \"first\\n{ \\\" // }\"}")
