module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_data: obj, _count: obj) : obj = null
let repeated_var: Val = FInt 1L
let single_var: Val = FList [
    FInt 4L;
    FInt 5L;
    FInt 6L
]
process(repeated_var, 1)
process(single_var, 0)
process(repeated_var, 8)
