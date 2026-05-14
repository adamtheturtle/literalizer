module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_value: obj, _count: obj) : obj = null
process(1, 42)
process(2, 100)
