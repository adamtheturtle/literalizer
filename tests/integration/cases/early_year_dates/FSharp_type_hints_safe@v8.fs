module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FDate of System.DateOnly
    | FDatetime of System.DateTime
let my_data: Val = FMap [
    ("date", FDate (System.DateOnly(99, 5, 27)));
    ("naive", FDatetime (System.DateTime(1, 1, 1, 12, 30, 0)));
    ("recent", FDatetime (System.DateTime(2024, 5, 27, 10, 0, 0)))
]
