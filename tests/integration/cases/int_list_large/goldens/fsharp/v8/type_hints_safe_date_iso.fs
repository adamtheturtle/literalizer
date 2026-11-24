module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 1000000L;
    FInt(-1234L);
    FInt 255L;
    FInt(-10L)
]
