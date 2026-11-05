module Main

type Val =
    | FInt of int64
    | FSet of Val list
let consume_widget (_arg_value: obj) : obj = null
consume_widget(FSet [
    FInt 1L;
    FInt 2L
]) |> ignore
