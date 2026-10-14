module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let shared: JsonNode = JsonObject(dict [
    ("value", (JsonArray([|(JsonValue.Create(1L) :> JsonNode); (JsonValue.Create(2L) :> JsonNode)|]) :> JsonNode))
])
consume((JsonObject(dict [("left", (shared :> JsonNode)); ("right", (shared :> JsonNode))]) :> JsonNode)) |> ignore
