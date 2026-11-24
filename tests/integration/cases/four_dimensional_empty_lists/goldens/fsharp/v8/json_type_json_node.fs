module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonArray([|(JsonArray([|(JsonArray() :> JsonNode)|]) :> JsonNode)|]) :> JsonNode);
    (JsonArray([|(JsonArray([|(JsonArray() :> JsonNode)|]) :> JsonNode)|]) :> JsonNode)
|])
