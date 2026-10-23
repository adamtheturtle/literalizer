module Main

type Val =
    | FInt of int64
    | FSet of Val list
let my_data: Val = FSet [
    FInt 0b1L;
    FInt 0b10L;
    FInt 0b11L
]
