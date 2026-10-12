module Main

let f (_a: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
f(FList [FInt 1L])
