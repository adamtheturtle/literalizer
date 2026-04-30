module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let x: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = FList [
    x;
    FInt 1L;
    FInt 2L
]
