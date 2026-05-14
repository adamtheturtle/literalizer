module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 0b1L;
    FInt 0b10L;
    FInt 0b11L
]
