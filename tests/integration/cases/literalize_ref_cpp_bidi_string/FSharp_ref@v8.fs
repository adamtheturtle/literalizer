module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let text: Val = FStr "a‪b"
let my_data: Val = FMap [
    ("value", text)
]
