module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_value: obj) : obj = null
process(FInt(-1L))
process(FInt(-2L))
process(FInt(-3L))
