module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // comment ending backslash \ .
    ("x", FInt 1L)
]
