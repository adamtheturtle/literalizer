module Main

type Val =
    | FInt of int64
    | FList of Val list
let consume_widget (_arg_value: obj) : obj = null
consume_widget(    FList [
        FInt 1L;
        FInt 2L
    ]) |> ignore
