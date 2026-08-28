module Main

let process (_xs: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
process(FList [
    FInt 1L;
    FInt 2L
])
process(FList [
    FInt 3L
])
