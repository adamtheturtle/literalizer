module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let myVar: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = myVar
