module Main

let make_widget (_Before: obj) : obj = null
type Val =
    | FInt of int64
make_widget(FInt 1L) |> ignore
