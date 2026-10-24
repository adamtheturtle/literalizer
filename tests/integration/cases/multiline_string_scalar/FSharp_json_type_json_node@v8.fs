module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonValue.Create("\nroot first line\n  indented\n\nroot last line\n")
