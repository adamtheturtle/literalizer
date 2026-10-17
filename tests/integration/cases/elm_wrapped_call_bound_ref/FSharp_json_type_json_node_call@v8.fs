module Main

open System.Text.Json.Nodes
let make_widget (_value: obj) : obj = null
let value: JsonNode = JsonValue.Create(1L)
make_widget(value) |> ignore
