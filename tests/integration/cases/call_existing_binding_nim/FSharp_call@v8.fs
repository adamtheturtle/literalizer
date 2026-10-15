module Main

type Val =
    | FInt of int64
let make_widget (_count: obj) : obj = null
let mutable my_data = make_widget(FInt 0L)
let my_data = make_widget(FInt 1L)
make_widget(my_data) |> ignore
