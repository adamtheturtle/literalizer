module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_value: obj, _count: obj) : obj = null
process(FInt 1L, FInt 42L)
process(FInt 2L, FInt 100L)
