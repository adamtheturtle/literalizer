module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FList [FList [FInt 1L]; FList [FInt 2L]]);
    ("b", FList [FList [FStr "x"]; FList [FStr "y"]])
]
