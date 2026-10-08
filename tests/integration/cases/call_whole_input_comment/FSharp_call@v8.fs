module Main

type Val =
    | FInt of int64
    | FList of Val list
let f (_a: obj) : obj = null
f(FList [FInt 1L])  // note
