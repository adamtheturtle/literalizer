module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let myVar: Val = FInt 0L
let my_data: Val = FMap [
    ("key", myVar)
]
