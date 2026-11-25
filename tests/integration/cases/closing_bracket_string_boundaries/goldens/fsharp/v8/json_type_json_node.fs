module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("]") :> JsonNode);
    (JsonValue.Create("a]") :> JsonNode);
    (JsonValue.Create("a]=") :> JsonNode);
    (JsonValue.Create("a]b") :> JsonNode)
|])
