module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("100% done") :> JsonNode);
    (JsonValue.Create("%(name) is here") :> JsonNode)
|])
