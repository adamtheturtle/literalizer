module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FDate of System.DateTime
    | FDatetime of System.DateTime
let my_data: Val = FMap [
    ("date", FStr (string (System.DateOnly(2024, 1, 15))));
    ("datetime", FStr (string (System.DateTime(2024, 1, 15, 12, 30, 0))))
]
