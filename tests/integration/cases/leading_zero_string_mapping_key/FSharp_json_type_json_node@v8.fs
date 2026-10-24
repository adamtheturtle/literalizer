module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("08", (JsonValue.Create("value") :> JsonNode))
])
