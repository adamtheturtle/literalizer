module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let refX: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = FList [
    refX;
    FInt 1L;
    FInt 2L
]
