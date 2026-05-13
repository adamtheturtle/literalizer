module Main

let make_widget (_count: obj) : obj = null
type Val =
    | FInt of int64
let result: Val = FInt make_widget(42)L
