module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("alpha", FList [FInt 2L; FList []]);
    ("beta", FList [FInt 5L; FList [FStr "x"]])
]
