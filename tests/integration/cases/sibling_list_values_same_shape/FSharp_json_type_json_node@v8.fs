module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("test", (JsonArray([|(JsonValue.Create(5L) :> JsonNode); (JsonArray([|(JsonValue.Create("compile") :> JsonNode); (JsonValue.Create("test") :> JsonNode)|]) :> JsonNode)|]) :> JsonNode));
    ("package", (JsonArray([|(JsonValue.Create(7L) :> JsonNode); (JsonArray([|(JsonValue.Create("link") :> JsonNode); (JsonValue.Create("test") :> JsonNode)|]) :> JsonNode)|]) :> JsonNode))
])
