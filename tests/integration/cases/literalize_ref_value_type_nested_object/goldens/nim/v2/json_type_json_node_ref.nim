import json
var shared: JsonNode = %*([
    1,
    2
])
var build: JsonNode = %*([
    1,
    2
])
var jsonObject: JsonNode = %*([
    1,
    2
])
var jsonAllocator: JsonNode = %*([
    1,
    2
])
var jsonEntries: JsonNode = %*([
    1,
    2
])
var jsonEntry: JsonNode = %*([
    1,
    2
])
var my_data: JsonNode = %*({
    "field": shared,
    "nested": %*([shared, newJObject()]),
    "build": build,
    "json_object": jsonObject,
    "json_allocator": jsonAllocator,
    "json_entries": jsonEntries,
    "json_entry": jsonEntry
})
