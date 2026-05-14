module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_value: obj) : obj = null
process(-1)
process(-2)
process(-3)
