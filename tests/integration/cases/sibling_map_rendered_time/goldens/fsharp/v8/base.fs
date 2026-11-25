module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FMap [("k", FStr (string (System.TimeOnly(7, 30, 0))))]);
    ("b", FMap [("k", FStr "string")])
]
