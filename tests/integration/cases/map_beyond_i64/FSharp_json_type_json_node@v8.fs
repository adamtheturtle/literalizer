module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("a", (JsonValue.Create(9223372036854775807L) :> JsonNode));
    ("b", (JsonValue.Create(9223372036854775808UL) :> JsonNode))
])
