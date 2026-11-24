module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("issue #{42}") :> JsonNode);
    (JsonValue.Create("color #red") :> JsonNode)
|])
