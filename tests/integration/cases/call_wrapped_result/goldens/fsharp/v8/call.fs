module Main

let make_widget (_value: obj) : obj = null
type Val =
    | FInt of int64
let my_data = make_widget(FInt 1L)
