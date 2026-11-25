module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonArray([|(JsonArray() :> JsonNode); (JsonArray() :> JsonNode)|]) :> JsonNode);
    (JsonArray([|(JsonArray([|(JsonValue.Create(1L) :> JsonNode)|]) :> JsonNode); (JsonArray([|(JsonValue.Create(1L) :> JsonNode)|]) :> JsonNode)|]) :> JsonNode)
|])
