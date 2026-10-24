module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("fffe", (JsonValue.Create("￾") :> JsonNode));
    ("ffff", (JsonValue.Create("￿") :> JsonNode))
])
