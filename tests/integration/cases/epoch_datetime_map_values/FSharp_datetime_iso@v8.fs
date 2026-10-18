module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("within_i32", FStr "2024-01-15T12:00:00");
    ("beyond_i32", FStr "2099-06-15T08:30:00")
]
