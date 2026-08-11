module Main

let process (_a: obj, _b: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
process(FInt 1L, FInt 2L)
process(FInt 3L, FInt 4L)
