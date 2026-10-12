module Main

type Val =
    | FInt of int64
let make_widget (_count: obj) : obj = null
let my_data: Val = FInt 42L
let my_data = make_widget(my_data) // note
// extra
make_widget(my_data)
