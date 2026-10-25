module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("__proto__", (JsonObject(dict [("x", (JsonValue.Create(1L) :> JsonNode))]) :> JsonNode));
    ("ordinary", (JsonValue.Create(2L) :> JsonNode))
])
