module Main

type Val =
    | FInt of int64
    | FList of Val list
let f (_a: obj) : obj = null
let x: Val = FInt 1L
f(x)
