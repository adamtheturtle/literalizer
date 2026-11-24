import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("[\"C:\\\\path\\\\to\\\\file\", \"back\\\\\\\\slash\", \"hello \\\\\\\"world\\\\\\\"\", \"path\\\\to \\\"# file\", \"trailing\\\\\", \"both \\\"quotes''' here\", \"line1\\\\nline2\\nwith newline\"]")
