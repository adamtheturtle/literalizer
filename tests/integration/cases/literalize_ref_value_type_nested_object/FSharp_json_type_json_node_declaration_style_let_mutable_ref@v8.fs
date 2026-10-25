module Main

open System.Text.Json.Nodes
let mutable shared: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let mutable build: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let mutable jsonObject: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let mutable jsonAllocator: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let mutable jsonEntries: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let mutable jsonEntry: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let mutable my_data: JsonNode = JsonObject(dict [
    ("field", (if isNull shared then null else (shared).DeepClone()));
    ("nested", (JsonArray([|(if isNull shared then null else (shared).DeepClone()); (JsonObject() :> JsonNode)|]) :> JsonNode));
    ("build", (if isNull build then null else (build).DeepClone()));
    ("json_object", (if isNull jsonObject then null else (jsonObject).DeepClone()));
    ("json_allocator", (if isNull jsonAllocator then null else (jsonAllocator).DeepClone()));
    ("json_entries", (if isNull jsonEntries then null else (jsonEntries).DeepClone()));
    ("json_entry", (if isNull jsonEntry then null else (jsonEntry).DeepClone()))
])
