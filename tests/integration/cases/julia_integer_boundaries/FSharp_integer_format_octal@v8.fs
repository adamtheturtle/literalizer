module Main

type Val =
    | FInt of int64
    | FBigInt of bigint
    | FList of Val list
let my_data: Val = FList [
    FInt(-0o1000000000000000000000L);
    FBigInt 0o1000000000000000000000I
]
