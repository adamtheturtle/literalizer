module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create(-0.0) :> JsonNode);
    (JsonValue.Create(1.5) :> JsonNode)
|])
