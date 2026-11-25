module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("value", (JsonValue.Create(0.0) :> JsonNode))
])
