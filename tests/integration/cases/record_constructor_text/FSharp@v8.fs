module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("text", FStr "Record0(");
    ("number", FInt 1L)
]
