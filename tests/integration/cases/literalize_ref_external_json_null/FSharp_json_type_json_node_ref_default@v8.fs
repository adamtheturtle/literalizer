module Main

open System.Text.Json.Nodes
let consume_widget (_arg_value: obj) : obj = null
do
    let item: JsonNode = null
    let mutable my_data: JsonNode = null
    consume_widget(my_data) |> ignore
    let my_data: JsonNode = item
    consume_widget(my_data) |> ignore
    ()
