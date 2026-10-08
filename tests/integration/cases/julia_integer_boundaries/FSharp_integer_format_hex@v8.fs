module Main

type Val =
    | FInt of bigint
    | FList of Val list
let my_data: Val = FList [
    FInt(-0x8000000000000000L);
    FInt 0x8000000000000000I
]
