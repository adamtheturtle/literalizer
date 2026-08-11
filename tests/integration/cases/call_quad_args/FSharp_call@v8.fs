module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_a: obj, _b: obj, _c: obj, _d: obj) : obj = null
process(FInt 1L, FInt 2L, FInt 3L, FInt 4L)
process(FInt 5L, FInt 6L, FInt 7L, FInt 8L)
