module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("morning", (JsonValue.Create("09:30:00") :> JsonNode));
    ("afternoon", (JsonValue.Create("14:15:00") :> JsonNode));
    ("evening", (JsonValue.Create("23:59:59") :> JsonNode))
])
