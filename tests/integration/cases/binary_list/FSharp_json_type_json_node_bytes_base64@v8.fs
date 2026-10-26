module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("SGVsbG8=") :> JsonNode)
|])
