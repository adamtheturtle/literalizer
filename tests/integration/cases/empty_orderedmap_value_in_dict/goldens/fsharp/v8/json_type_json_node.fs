module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("a", (JsonObject() :> JsonNode));
    ("b", (JsonValue.Create(1L) :> JsonNode))
])
