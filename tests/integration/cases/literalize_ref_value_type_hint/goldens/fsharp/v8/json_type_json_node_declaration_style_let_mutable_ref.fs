module Main

open System.Text.Json.Nodes
let mutable refData: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let mutable my_data: JsonNode = refData
