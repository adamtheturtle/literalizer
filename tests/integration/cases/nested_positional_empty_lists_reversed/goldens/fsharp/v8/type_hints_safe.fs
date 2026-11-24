module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FList [FList [FInt 1L]];
    FList [FList []]
]
