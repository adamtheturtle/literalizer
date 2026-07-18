module Main

type Val =
    | FInt of bigint
    | FList of Val list
let my_data: Val = FList [
    FInt 9223372036854775807L;
    FInt 9223372036854775808I
]
