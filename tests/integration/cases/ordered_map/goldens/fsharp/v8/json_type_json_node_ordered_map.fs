module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("name", (JsonValue.Create("Alice") :> JsonNode));
    ("age", (JsonValue.Create(30L) :> JsonNode));
    ("active", (JsonValue.Create(true) :> JsonNode))
])
