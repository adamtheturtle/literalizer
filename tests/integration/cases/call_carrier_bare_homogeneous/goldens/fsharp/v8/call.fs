module Main

let make_widget (_first_value: obj, _second_value: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
make_widget(FList [FInt 1L], FList [FInt 2L]) |> ignore
