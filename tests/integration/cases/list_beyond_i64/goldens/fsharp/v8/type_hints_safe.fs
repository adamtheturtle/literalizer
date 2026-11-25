module Main

type Val =
    | FInt of int64
    | FBigInt of bigint
    | FList of Val list
let my_data: Val = FList [
    FInt 9223372036854775807L;
    FBigInt 9223372036854775808I
]
