module Main

type Val =
    | FInt of int64
    | FList of Val list
let consume_widget (__arg: obj) : obj = null
let ref_data: Val = FList [
    FInt 1L;
    FInt 2L
]
let my_data: Val = FList [
    FInt 0L
]
consume_widget(my_data) |> ignore
let my_data: Val = ref_data
consume_widget(my_data) |> ignore
