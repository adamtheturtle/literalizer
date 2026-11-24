import json
let shared: JsonNode = %*([
    1,
    2
])
let build: JsonNode = %*([
    1,
    2
])
let jsonObject: JsonNode = %*([
    1,
    2
])
let jsonAllocator: JsonNode = %*([
    1,
    2
])
let jsonEntries: JsonNode = %*([
    1,
    2
])
let jsonEntry: JsonNode = %*([
    1,
    2
])
let my_data: JsonNode = %*({
    "field": shared,
    "nested": %*([shared, newJObject()]),
    "build": build,
    "json_object": jsonObject,
    "json_allocator": jsonAllocator,
    "json_entries": jsonEntries,
    "json_entry": jsonEntry
})
