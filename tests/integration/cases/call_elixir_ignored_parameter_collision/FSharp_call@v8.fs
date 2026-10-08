module Main

let f (_x: obj, __x: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
f(FInt 1L, FInt 2L)
