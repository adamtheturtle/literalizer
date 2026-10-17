module Main

type Val =
    | FInt of int64
    | FList of Val list
let existing: Val = FInt 1L
let my_data: Val = FList [
    FInt 0L;
    FList [FList [existing]]
]
