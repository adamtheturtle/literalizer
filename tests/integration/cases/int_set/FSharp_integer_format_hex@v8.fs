module Main

type Val =
    | FInt of int64
    | FSet of Val list
let my_data: Val = FSet [
    FInt 0x1L;
    FInt 0x2L;
    FInt 0x3L
]
