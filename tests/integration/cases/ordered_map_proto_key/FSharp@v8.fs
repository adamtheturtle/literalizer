module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("__proto__", FMap [("x", FInt 1L)]);
    ("ordinary", FInt 2L)
]
