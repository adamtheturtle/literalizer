module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let other: Val = FStr "true"
let my_data: Val = FMap [
    ("main", FMap [("x", FInt 1L); ("y", FStr "s")])
]
