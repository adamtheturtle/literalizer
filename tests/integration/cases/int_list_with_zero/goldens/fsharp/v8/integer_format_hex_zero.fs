module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 0x0L;
    FInt 0x1L;
    FInt(-0x1L)
]
