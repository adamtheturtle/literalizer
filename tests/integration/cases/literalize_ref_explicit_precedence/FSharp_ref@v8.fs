module Main

type Val =
    | FInt of int64
    | FList of Val list
let x: Val = FList [
    FInt 1L;
    FInt 2L
]
let my_data: Val = x
