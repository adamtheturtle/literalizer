module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("starts_at", (JsonValue.Create("09:30:00") :> JsonNode))
])
