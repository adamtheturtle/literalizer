module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("中中中中中中中中中中中中中中中中中中中中") :> JsonNode);
    (JsonValue.Create("é'é'é'é'é'é'é'é'é'é'") :> JsonNode);
    (JsonValue.Create("🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂") :> JsonNode)
|])
