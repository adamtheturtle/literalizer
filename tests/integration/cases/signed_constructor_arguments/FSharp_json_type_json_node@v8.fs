module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create(-42L) :> JsonNode);
    (JsonValue.Create(0L) :> JsonNode);
    (JsonValue.Create(42L) :> JsonNode);
    (JsonValue.Create(-1.25) :> JsonNode);
    (JsonValue.Create(0.0) :> JsonNode);
    (JsonValue.Create(1.25) :> JsonNode)
|])
