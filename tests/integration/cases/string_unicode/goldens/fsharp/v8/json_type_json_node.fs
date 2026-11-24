module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("café") :> JsonNode);
    (JsonValue.Create("中文") :> JsonNode);
    (JsonValue.Create("😀") :> JsonNode)
|])
