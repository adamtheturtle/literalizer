module Main

let f (_value: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
f(FList [FInt 1L; FInt 2L])
