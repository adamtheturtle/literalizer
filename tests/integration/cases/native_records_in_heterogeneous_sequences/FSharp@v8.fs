module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("h", FList [FInt 1L; FStr "a"; FList [FInt 2L; FStr "b"]; FMap [("k", FList [FBool true])]])
]
