module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonArray([|(JsonValue.Create("\nfirst line\n  indented\n\nlast line\n") :> JsonNode)|]) :> JsonNode)
|])
