module Main

let ``process`` (_value: obj) : obj = null
type Val =
    | FInt of int64
let my_data = ``process``(FInt 1L)
