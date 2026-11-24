module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FList [FList [FInt 1L; FStr "value"]; FList []];
    FList [FList []; FList [FInt 2L; FStr "other"]]
]
