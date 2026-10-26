module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonObject(dict [("", (JsonValue.Create("external_value") :> JsonNode))]) :> JsonNode)
|])
