module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 999999999999999999L;
    FInt(-999999999999999999L)
]
