module Main

type Val =
    | FInt of int64
    | FBigInt of bigint
    | FList of Val list
let my_data: Val = FList [
    FList [FInt 1L];
    FList [FBigInt 1180591620717411303424I]
]
