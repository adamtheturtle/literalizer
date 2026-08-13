module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let myVar: Val = FInt 1L
let my_data: Val = FMap [
    ("key", myVar)
]
