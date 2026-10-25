module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("1960-01-01T00:00:00+00:00") :> JsonNode)
|])
