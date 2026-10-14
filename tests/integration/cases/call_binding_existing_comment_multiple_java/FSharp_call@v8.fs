module Main

type Val =
    | FNull
    | FInt of int64
let make_widget (_count: obj) : obj = null
let mutable my_data = make_widget(FNull)
let my_data = make_widget(FInt 42L) // note
// extra
