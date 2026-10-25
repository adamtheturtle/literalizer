module Main

open System.Text.Json.Nodes
let shared: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let build: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let jsonObject: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let jsonAllocator: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let jsonEntries: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let jsonEntry: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let my_data: JsonNode = JsonObject(dict [
    ("field", (if isNull shared then null else (shared).DeepClone()));
    ("nested", (JsonArray([|(if isNull shared then null else (shared).DeepClone()); (JsonObject() :> JsonNode)|]) :> JsonNode));
    ("build", (if isNull build then null else (build).DeepClone()));
    ("json_object", (if isNull jsonObject then null else (jsonObject).DeepClone()));
    ("json_allocator", (if isNull jsonAllocator then null else (jsonAllocator).DeepClone()));
    ("json_entries", (if isNull jsonEntries then null else (jsonEntries).DeepClone()));
    ("json_entry", (if isNull jsonEntry then null else (jsonEntry).DeepClone()))
])
