module Main

type Val =
    | FFloat of float
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("pi", FFloat 3.141592653589793)
]
