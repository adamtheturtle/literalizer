module Main

open System.Text.Json.Nodes
let mutable shared: JsonNode = JsonObject(dict [
    ("field", (JsonArray([|(JsonValue.Create(1L) :> JsonNode); (JsonValue.Create(2L) :> JsonNode)|]) :> JsonNode))
])
let mutable my_data: JsonNode = shared
