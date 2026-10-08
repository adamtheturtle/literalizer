module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FInt 1L);  // inline ending backslash \ .
    ("b", FInt 2L)
]
