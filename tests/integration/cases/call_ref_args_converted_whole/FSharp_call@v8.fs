module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_data: obj) : obj = null
let myVar: Val = FList [
    FInt 1L;
    FInt 2L;
    FInt 3L
]
process(myVar)
