module Main

type Val =
    | FInt of int64
    | FList of Val list
let consume_widget (_arg_value: obj) : obj = null
let a: Val = FInt 0L
let my_data: Val = FList [
    a;
    FInt 1L
]
consume_widget(my_data) |> ignore
