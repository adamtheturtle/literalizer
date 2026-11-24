module Main

type Val =
    | FInt of int64
    | FList of Val list
let seed: Val = FInt 1L
let my_data: Val = FList [
    FList [];
    FList [FList []];
    seed
]
