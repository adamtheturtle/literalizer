module Main

open System.Text.Json.Nodes
let make_widget (_count: obj) : obj = null
let consume (_count: obj) : obj = null
do
    let mutable my_data = make_widget((JsonValue.Create(7L) :> JsonNode))
    consume(my_data) |> ignore
    let my_data = (
        if make_widget((JsonValue.Create(13L) :> JsonNode)) <> null then
            make_widget((JsonValue.Create(13L) :> JsonNode)) // inner
        else null
    ) // trailing
    consume(my_data) |> ignore
    ()
