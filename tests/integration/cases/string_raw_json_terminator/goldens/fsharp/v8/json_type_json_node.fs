module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    (")json", (JsonValue.Create("x") :> JsonNode))
])
