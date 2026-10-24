module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FDatetime of System.DateTime
let my_data: Val = FMap [
    ("date", FStr "0099-05-27");
    ("naive", FDatetime (System.DateTime(1, 1, 1, 12, 30, 0)));
    ("recent", FDatetime (System.DateTime(2024, 5, 27, 10, 0, 0)))
]
