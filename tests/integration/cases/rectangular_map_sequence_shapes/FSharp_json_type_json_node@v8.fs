module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("a", (JsonArray([|(JsonObject(dict [("item", (JsonArray([|(JsonValue.Create(1L) :> JsonNode)|]) :> JsonNode))]) :> JsonNode)|]) :> JsonNode));
    ("b", (JsonArray([|(JsonObject(dict [("item", (JsonArray([|(JsonValue.Create(2L) :> JsonNode)|]) :> JsonNode))]) :> JsonNode)|]) :> JsonNode))
])
