module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("2024-01-15") :> JsonNode);
    (JsonValue.Create("2024-06-01") :> JsonNode)
|])
