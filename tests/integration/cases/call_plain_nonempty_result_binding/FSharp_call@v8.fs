module Main

let make_widget (_value: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
let my_data = make_widget(FList [FInt 1L])
