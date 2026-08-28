module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("$key", (JsonValue.Create("a\"b\tcé #{world} $ident") :> JsonNode));
    ("trailing multi-byte", (JsonValue.Create("café") :> JsonNode))
])
