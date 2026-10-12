module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let shared: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
consume((JsonObject(dict [("field", (shared :> JsonNode))]) :> JsonNode))
consume(shared)
