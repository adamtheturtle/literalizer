module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonValue.Create("hello \"world\" -- not a comment")
