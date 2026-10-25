module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    | FSet of Val list
let my_data: Val = FMap [
    ("a", FList []);
    ("b", FSet [FInt 1L; FInt 2L])
]
