module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("explicit_string", FStr "5");
    ("six", FStr "explicitly tagged key")
]
