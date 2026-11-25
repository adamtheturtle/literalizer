module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("within_i32", (JsonValue.Create("2024-01-15T12:00:00") :> JsonNode));
    ("beyond_i32", (JsonValue.Create("2099-06-15T08:30:00") :> JsonNode))
])
