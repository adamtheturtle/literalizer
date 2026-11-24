module Main

open System.Text.Json.Nodes
let consume_widget (_arg_value: obj) : obj = null
do
    let shared: JsonNode = JsonArray([|
        (JsonValue.Create(1L) :> JsonNode);
        (JsonValue.Create(2L) :> JsonNode)
    |])
    let mutable my_data: JsonNode = JsonArray([|
        (JsonValue.Create(0L) :> JsonNode)
    |])
    consume_widget(my_data) |> ignore
    let my_data: JsonNode = shared
    consume_widget(my_data) |> ignore
    ()
