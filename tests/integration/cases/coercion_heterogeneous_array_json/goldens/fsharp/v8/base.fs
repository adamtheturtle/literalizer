module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FInt 1L;
    FFloat 2.5;
    FInt 3L
]
