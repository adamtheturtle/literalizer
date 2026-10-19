module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("x", FList [FInt 1L; FList [FInt 2L; FList [FInt 3L]]])
]
