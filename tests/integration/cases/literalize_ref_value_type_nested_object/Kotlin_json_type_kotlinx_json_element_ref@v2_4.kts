import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
val shared: JsonElement = Json.parseToJsonElement("[1, 2]")
val build: JsonElement = Json.parseToJsonElement("[1, 2]")
val jsonObject: JsonElement = Json.parseToJsonElement("[1, 2]")
val jsonAllocator: JsonElement = Json.parseToJsonElement("[1, 2]")
val jsonEntries: JsonElement = Json.parseToJsonElement("[1, 2]")
val jsonEntry: JsonElement = Json.parseToJsonElement("[1, 2]")
val my_data: JsonElement = Json.parseToJsonElement("{\"field\": [1, 2], \"nested\": [[1, 2], {}], \"build\": [1, 2], \"json_object\": [1, 2], \"json_allocator\": [1, 2], \"json_entries\": [1, 2], \"json_entry\": [1, 2]}")
