module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create(9223372036854775807L) :> JsonNode);
    (JsonValue.Create(9223372036854775808UL) :> JsonNode)
|])
