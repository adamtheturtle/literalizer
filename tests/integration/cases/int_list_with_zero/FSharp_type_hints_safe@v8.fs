module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 0L;
    FInt 1L;
    FInt(-1L)
]
