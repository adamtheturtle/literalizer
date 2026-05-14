module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_data: obj, _count: obj) : obj = null
let myVar: Val = FList [
    FInt 1L;
    FInt 2L;
    FInt 3L
]
let myOther: Val = FList [
    FInt 4L;
    FInt 5L;
    FInt 6L
]
process(myVar, 42)
process(myOther, 7)
