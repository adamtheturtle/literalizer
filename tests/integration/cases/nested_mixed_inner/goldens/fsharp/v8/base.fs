module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FList [FInt 1L; FStr "a"];
    FList [FInt 2L; FStr "b"]
]
