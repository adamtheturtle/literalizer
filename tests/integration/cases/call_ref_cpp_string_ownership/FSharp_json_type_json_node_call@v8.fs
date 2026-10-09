module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let item: JsonNode = JsonValue.Create("s")
consume(item)
