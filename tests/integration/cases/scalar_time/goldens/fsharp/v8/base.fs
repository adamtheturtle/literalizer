module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("starts_at", FStr (string (System.TimeOnly(9, 30, 0))))
]
