module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create(5.0e-324) :> JsonNode);
    (JsonValue.Create(-5.0e-324) :> JsonNode);
    (JsonValue.Create(1.0e-310) :> JsonNode)
|])
