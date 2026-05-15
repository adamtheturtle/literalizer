module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FDatetime of System.DateTime
let my_data: Val = FMap [
    ("within_i32", FStr (string (System.DateTime(2024, 1, 15, 12, 0, 0))));
    ("beyond_i32", FStr (string (System.DateTime(2099, 6, 15, 8, 30, 0))))
]
