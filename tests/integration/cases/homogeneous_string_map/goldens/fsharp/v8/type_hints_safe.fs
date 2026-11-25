module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FStr "x");
    ("b", FStr "y")
]
