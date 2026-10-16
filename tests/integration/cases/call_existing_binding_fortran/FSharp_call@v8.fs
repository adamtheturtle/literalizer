module Main

type Val =
    | FInt of int64
let make_widget (_count: obj) : obj = null
let consume_widget (_count: obj) : obj = null
let mutable my_data = make_widget(FInt 0L)
consume_widget(my_data) |> ignore
let my_data = make_widget(FInt 1L)
consume_widget(my_data) |> ignore
