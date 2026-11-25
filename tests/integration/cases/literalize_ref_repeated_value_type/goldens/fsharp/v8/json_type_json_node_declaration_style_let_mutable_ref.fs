module Main

open System.Text.Json.Nodes
let mutable shared: JsonNode = JsonValue.Create(42L)
let mutable my_data: JsonNode = JsonArray([|
    (if isNull shared then null else (shared).DeepClone());
    (if isNull shared then null else (shared).DeepClone())
|])
