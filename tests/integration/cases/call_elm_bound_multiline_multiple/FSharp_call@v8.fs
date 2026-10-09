module Main

type Val =
    | FInt of int64
    | FList of Val list
let f (_value: obj) : obj = null
let ref_data: Val = FList [
    FInt 1L;
    FInt 2L
]
f(FList [
    ref_data
])
f(FList [
    ref_data
])
