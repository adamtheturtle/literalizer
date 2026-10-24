module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let shared: JsonNode = JsonArray([|
    (JsonValue.Create(1L) :> JsonNode);
    (JsonValue.Create(2L) :> JsonNode)
|])
consume((JsonObject(dict [("field", (if isNull shared then null else (shared).DeepClone())); ("nested", (JsonArray([|(if isNull shared then null else (shared).DeepClone()); (JsonObject() :> JsonNode)|]) :> JsonNode))]) :> JsonNode)) |> ignore
