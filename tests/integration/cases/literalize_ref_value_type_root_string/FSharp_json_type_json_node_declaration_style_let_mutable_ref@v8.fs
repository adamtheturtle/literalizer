module Main

open System.Text.Json.Nodes
let mutable shared: JsonNode = JsonValue.Create("value")
let mutable my_data: JsonNode = shared
