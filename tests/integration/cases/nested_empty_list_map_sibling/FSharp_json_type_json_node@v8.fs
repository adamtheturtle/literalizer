module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonObject(dict [("values", (JsonArray() :> JsonNode))]) :> JsonNode);
    (JsonObject() :> JsonNode)
|])
