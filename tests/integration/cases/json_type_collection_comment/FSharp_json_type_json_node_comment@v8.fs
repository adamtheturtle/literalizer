module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("a", (JsonValue.Create(1L) :> JsonNode));  // About a.
    ("b", (JsonValue.Create(2L) :> JsonNode))
])
