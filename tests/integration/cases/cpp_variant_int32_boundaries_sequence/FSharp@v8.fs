module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt(-2147483648L);
    FInt(-2147483647L);
    FList [FInt 0L]
]
