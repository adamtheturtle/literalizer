module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("cr", (JsonValue.Create("a\rb") :> JsonNode));
    ("crlf", (JsonValue.Create("a\r\nb") :> JsonNode));
    ("lf", (JsonValue.Create("a\nb") :> JsonNode))
])
