module Main

open System.Text.Json.Nodes
let ZKV: JsonNode = JsonObject(dict [
    ("a", (JsonValue.Create(1L) :> JsonNode))
])
