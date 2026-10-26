module Main

type Val =
    | FInt of int64
    | FList of Val list
let make_widget (_value: obj) : obj = null
let consume (_value: obj) : obj = null
let my_data = make_widget(FInt 42L)
consume(my_data) |> ignore
