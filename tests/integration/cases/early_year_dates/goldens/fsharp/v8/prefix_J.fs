module Main

type Val =
    | JStr of string
    | JMap of (string * Val) list
    | JDate of System.DateOnly
    | JDatetime of System.DateTime
let my_data: Val = JMap [
    ("date", JDate (System.DateOnly(99, 5, 27)));
    ("naive", JDatetime (System.DateTime(1, 1, 1, 12, 30, 0)));
    ("recent", JDatetime (System.DateTime(2024, 5, 27, 10, 0, 0)))
]
