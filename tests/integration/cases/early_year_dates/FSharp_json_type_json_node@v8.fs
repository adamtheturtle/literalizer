module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("date", (JsonValue.Create("0099-05-27") :> JsonNode));
    ("naive", (JsonValue.Create("0001-01-01T12:30:00") :> JsonNode));
    ("recent", (JsonValue.Create("2024-05-27T10:00:00") :> JsonNode))
])
