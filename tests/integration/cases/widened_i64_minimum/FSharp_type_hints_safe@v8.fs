module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt(-9223372036854775808L);
    FInt 5L
]
