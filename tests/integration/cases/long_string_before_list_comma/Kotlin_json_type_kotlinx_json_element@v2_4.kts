import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val my_data: JsonElement = Json.parseToJsonElement("[\"This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.\", 1]")
