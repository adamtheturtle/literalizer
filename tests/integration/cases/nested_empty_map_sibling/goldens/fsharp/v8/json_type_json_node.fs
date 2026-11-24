module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonObject(dict [("mapping", (JsonObject() :> JsonNode))]) :> JsonNode);
    (JsonObject() :> JsonNode)
|])
