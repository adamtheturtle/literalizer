module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("times", (JsonArray([|(JsonValue.Create("09:30:00") :> JsonNode); (JsonValue.Create("17:45:00") :> JsonNode); (JsonValue.Create("23:59:59") :> JsonNode)|]) :> JsonNode))
])
