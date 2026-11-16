module Main

type Val =
    | FInt of int64
    | FList of Val list
let consume_widget (_arg_value: obj) : obj = null
do
    let mutable my_data: Val = FInt 0L
    let shared: Val = FInt 1L
    consume_widget(my_data) |> ignore
    let my_data: Val = shared
    consume_widget(my_data) |> ignore
    ()
