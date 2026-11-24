module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("outer", (JsonArray([|(JsonArray([|(JsonValue.Create("nested first line\n  indented\n\nnested last line\n") :> JsonNode)|]) :> JsonNode)|]) :> JsonNode))
])
