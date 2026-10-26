module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("48656c6c6f") :> JsonNode)
|])
