module Main

type Val =
    | FInt of int64
let make_widget (_value: obj) : obj = null
let value: Val = FInt 1L
make_widget(value) |> ignore
