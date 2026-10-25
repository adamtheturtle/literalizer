import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
var shared: JsonElement = Json.parseToJsonElement("[1, 2]")
var build: JsonElement = Json.parseToJsonElement("[1, 2]")
var jsonObject: JsonElement = Json.parseToJsonElement("[1, 2]")
var jsonAllocator: JsonElement = Json.parseToJsonElement("[1, 2]")
var jsonEntries: JsonElement = Json.parseToJsonElement("[1, 2]")
var jsonEntry: JsonElement = Json.parseToJsonElement("[1, 2]")
var my_data: JsonElement = Json.parseToJsonElement("{\"field\": [1, 2], \"nested\": [[1, 2], {}], \"build\": [1, 2], \"json_object\": [1, 2], \"json_allocator\": [1, 2], \"json_entries\": [1, 2], \"json_entry\": [1, 2]}")
