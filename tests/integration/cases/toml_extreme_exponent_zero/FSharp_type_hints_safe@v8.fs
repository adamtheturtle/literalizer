module Main

type Val =
    | FFloat of float
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("value", FFloat 0.0)
]
