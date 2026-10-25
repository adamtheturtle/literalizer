module Main

open System.Text.Json.Nodes
let consume_widget (_arg_value: obj) : obj = null
do
    let mutable my_data: JsonNode = JsonObject(dict [
        ("a", (JsonValue.Create(0L) :> JsonNode))
    ])
    consume_widget(my_data) |> ignore
    let my_data: JsonNode = JsonObject(dict [
        ("a", (JsonValue.Create(1L) :> JsonNode))
    ])
    consume_widget(my_data) |> ignore
    ()
