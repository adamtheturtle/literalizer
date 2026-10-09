module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let k: Val = FMap [
    ("a", FInt 1L)
]
