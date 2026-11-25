module Main

let make_widget (_first_value: obj) : obj = null
type Val =
    | FInt of int64
make_widget(FInt 1L) |> ignore
