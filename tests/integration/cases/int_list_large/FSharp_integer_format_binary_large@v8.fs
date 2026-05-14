module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 0b11110100001001000000L;
    FInt(-0b10011010010L);
    FInt 0b11111111L;
    FInt(-0b1010L)
]
