module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("date", (JsonValue.Create("2024-01-15") :> JsonNode));
    ("datetime", (JsonValue.Create("2024-01-15T12:30:00+00:00") :> JsonNode))
])
