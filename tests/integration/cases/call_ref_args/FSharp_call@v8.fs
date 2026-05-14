module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_data: obj, _count: obj) : obj = null
let my_var: Val = FList [
    FInt 1L;
    FInt 2L;
    FInt 3L
]
let my_other: Val = FList [
    FInt 4L;
    FInt 5L;
    FInt 6L
]
process(my_var, 42)
process(my_other, 7)
