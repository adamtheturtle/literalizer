module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FInt 0L;
    FList [FList [FStr "plain"]]
]
