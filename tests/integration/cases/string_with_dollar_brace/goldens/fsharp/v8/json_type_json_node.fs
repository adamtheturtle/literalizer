module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("prefix ${HOME} suffix") :> JsonNode);
    (JsonValue.Create("${interpolated}") :> JsonNode)
|])
