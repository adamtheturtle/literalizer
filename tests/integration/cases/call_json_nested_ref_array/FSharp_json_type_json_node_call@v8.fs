module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let shared: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
consume((JsonArray([|(if isNull shared then null else (shared).DeepClone()); (JsonValue.Create(42L) :> JsonNode)|]) :> JsonNode)) |> ignore
