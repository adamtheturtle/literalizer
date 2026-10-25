module Main

open System.Text.Json.Nodes
let userObj: JsonNode = JsonObject(dict [
    ("_", (JsonValue.Create("_") :> JsonNode))
])
let my_data: JsonNode = userObj
