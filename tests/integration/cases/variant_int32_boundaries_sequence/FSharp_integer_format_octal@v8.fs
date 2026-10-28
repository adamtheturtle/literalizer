module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt(-0o20000000000L);
    FInt(-0o17777777777L);
    FList [FInt 0o0L]
]
