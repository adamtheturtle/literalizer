module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 0xde0b6b3a763ffffL;
    FInt(-0xde0b6b3a763ffffL)
]
