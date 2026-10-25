module Main

type Val =
    | FInt of int64
    | FList of Val list
let consume_widget (_arg_value: obj) : obj = null
do
    let shared: Val = FList [
        FInt 1L;
        FInt 2L
    ]
    let mutable my_data: Val = FList [
        FInt 0L
    ]
    consume_widget(my_data) |> ignore
    let my_data: Val = shared
    consume_widget(my_data) |> ignore
    ()
