module Main

type Val =
    | FList of Val list
    | FInt of int64
let my_data: Val = FList [
    FInt 1705321800L;
    FInt 1717228800L
]
