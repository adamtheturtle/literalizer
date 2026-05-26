module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonArray([|(JsonValue.Create(1L) :> JsonNode); (JsonValue.Create("a") :> JsonNode)|]) :> JsonNode);
    (JsonArray([|(JsonValue.Create(2L) :> JsonNode); (JsonValue.Create("b") :> JsonNode)|]) :> JsonNode)
|])
