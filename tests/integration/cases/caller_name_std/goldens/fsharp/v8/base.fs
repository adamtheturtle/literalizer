module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let std: Val = FMap [
    ("a", FInt 1L)
]
