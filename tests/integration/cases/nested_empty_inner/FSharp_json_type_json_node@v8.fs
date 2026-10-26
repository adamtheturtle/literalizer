module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonArray() :> JsonNode);
    (JsonArray() :> JsonNode)
|])
