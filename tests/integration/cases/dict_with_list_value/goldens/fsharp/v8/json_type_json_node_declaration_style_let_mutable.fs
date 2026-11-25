module Main

open System.Text.Json.Nodes
let mutable my_data: JsonNode = JsonObject(dict [
    ("name", (JsonValue.Create("Alice") :> JsonNode));
    ("scores", (JsonArray([|(JsonValue.Create(10L) :> JsonNode); (JsonValue.Create(20L) :> JsonNode); (JsonValue.Create(30L) :> JsonNode)|]) :> JsonNode))
])
