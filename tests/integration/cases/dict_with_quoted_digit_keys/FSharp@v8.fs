module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("0a", FStr "first");
    ("1b", FStr "second")
]
