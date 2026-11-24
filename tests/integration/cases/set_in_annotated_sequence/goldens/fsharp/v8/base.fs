module Main

type Val =
    | FInt of int64
    | FList of Val list
    | FSet of Val list
let my_data: Val = FList [
    FSet [];
    FSet [FInt 1L; FInt 2L];
    FList []
]
