module Main

let make_widget (_items: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
let my_data = make_widget(FList [FList [FInt 1L; FInt 2L]; FList [FInt 3L]])
