module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let bound: Val = FInt 2L
let my_data: Val = FMap [
    ("value", bound)
]
