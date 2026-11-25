module Main

type Val =
    | FNull
    | FList of Val list
let consume_widget (_arg_value: obj) : obj = null
do
    let item: Val = FNull
    let mutable my_data: Val = FNull
    consume_widget(my_data) |> ignore
    let my_data: Val = item
    consume_widget(my_data) |> ignore
    ()
