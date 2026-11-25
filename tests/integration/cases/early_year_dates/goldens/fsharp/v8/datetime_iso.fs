module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FDate of System.DateOnly
let my_data: Val = FMap [
    ("date", FDate (System.DateOnly(99, 5, 27)));
    ("naive", FStr "0001-01-01T12:30:00");
    ("recent", FStr "2024-05-27T10:00:00")
]
