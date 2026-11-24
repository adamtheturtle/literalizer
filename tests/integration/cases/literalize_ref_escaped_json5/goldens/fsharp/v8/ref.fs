module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let existing: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = existing
