module Main

type Val =
    | FInt of int64
    | FList of Val list
let make_widget (_first: obj, _second: obj) : obj = null
let consume (_first: obj, _second: obj) : obj = null
let my_data = make_widget(FInt 42L, FInt 3L)
consume(FInt 3L, my_data) |> ignore
