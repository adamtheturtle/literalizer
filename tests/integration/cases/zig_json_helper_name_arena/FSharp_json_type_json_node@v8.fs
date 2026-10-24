module Main

open System.Text.Json.Nodes
let arena: JsonNode = JsonObject(dict [
    ("a", (JsonValue.Create(1L) :> JsonNode))
])
