module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("1901-12-13T20:45:51") :> JsonNode);
    (JsonValue.Create("1901-12-13T20:45:52") :> JsonNode);
    (JsonValue.Create("2038-01-19T03:14:07") :> JsonNode);
    (JsonValue.Create("2038-01-19T03:14:08") :> JsonNode)
|])
