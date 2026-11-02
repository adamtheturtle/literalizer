module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // event time
    ("when", FStr "2024-01-15T12:34:56+00:00")
]
