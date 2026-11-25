module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("price $10") :> JsonNode);
    (JsonValue.Create("$HOME") :> JsonNode)
|])
