module Main

open System.Text.Json.Nodes
let refData: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
let my_data: JsonNode = refData
