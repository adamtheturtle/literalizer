module Main

open System.Text.Json.Nodes
let shared: JsonNode = JsonValue.Create(42L)
let my_data: JsonNode = JsonObject(dict [
    ("refs", (JsonArray([|(if isNull shared then null else (shared).DeepClone()); (if isNull shared then null else (shared).DeepClone())|]) :> JsonNode));
    ("quoted", (JsonValue.Create("#{shared}") :> JsonNode))
])
