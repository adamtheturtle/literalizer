module Main

type Val =
    | FInt of int64
    | FList of Val list
let capture (___proto__: obj) : obj = null
capture(FInt 1L)
