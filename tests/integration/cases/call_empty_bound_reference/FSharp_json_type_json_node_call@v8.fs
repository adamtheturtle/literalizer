module Main

open System.Text.Json.Nodes
let make_widget (_value: obj) : obj = null
let items: JsonNode = JsonArray()
make_widget(items) |> ignore
