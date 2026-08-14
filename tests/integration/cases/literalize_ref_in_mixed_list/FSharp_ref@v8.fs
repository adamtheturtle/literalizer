module Main

type Val =
    | FInt of int64
    | FList of Val list
let refX: Val = FInt 3L
let my_data: Val = FList [
    refX;
    FInt 1L;
    FInt 2L
]
