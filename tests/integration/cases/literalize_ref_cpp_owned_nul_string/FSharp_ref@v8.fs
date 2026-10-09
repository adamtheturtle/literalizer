module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let shared: Val = FStr "a\000b"
let my_data: Val = FMap [
    ("value", shared)
]
