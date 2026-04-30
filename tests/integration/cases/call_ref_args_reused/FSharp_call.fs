module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_data: obj, _count: obj) : obj = null
let shared: Val = FInt 1L
let other: Val = FInt 2L
process(shared, 1)
process(other, 0)
process(shared, 8)
