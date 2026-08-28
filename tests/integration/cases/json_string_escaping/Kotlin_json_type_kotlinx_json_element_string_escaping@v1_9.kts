import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("{\"\$key\": \"a\\\"b\\tcé #{world} \$ident\", \"trailing multi-byte\": \"café\"}")
