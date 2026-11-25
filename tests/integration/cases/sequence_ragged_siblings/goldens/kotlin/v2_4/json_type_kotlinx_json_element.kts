import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("[[\"set_task\", \"web\", \"lint_web\"], [\"merge_pipelines\"]]")
