module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("_", FList [FInt 1L; FFloat 2.5; FInt 3L])
]
