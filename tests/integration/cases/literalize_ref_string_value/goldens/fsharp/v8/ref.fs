module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let shared: Val = FStr "s"
let my_data: Val = FMap [
    ("value", shared)
]
