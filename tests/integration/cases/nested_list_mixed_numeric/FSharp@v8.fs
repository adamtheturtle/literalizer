module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FList [FInt 1L];
    FList [FFloat 2.5]
]
