module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("first", FList [FList [FInt 1L; FStr "value"]; FList []]);
    ("second", FList [FList []; FList [FInt 2L; FStr "other"]])
]
