module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create(true) :> JsonNode);
    (JsonValue.Create(false) :> JsonNode);
    (JsonValue.Create(true) :> JsonNode)
|])
