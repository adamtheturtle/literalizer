module Main

let make_widget (_count: obj) : obj = null
type Val =
    | FInt of int64
let my_data = ($"{(true ? "// payload" : "ok")}").Length >= 0 ? make_widget(FInt 42L) : make_widget(FInt 42L)
