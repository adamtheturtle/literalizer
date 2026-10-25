module Main

type Val =
    | FInt of int64
    | FList of Val list
let consume_widget (_arg_value: obj) : obj = null
let shared: Val = FInt 1L
let my_data: Val = shared
consume_widget(my_data) |> ignore
