module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FDate of System.DateOnly
let my_data: Val = FMap [
    ("a", FMap [("k", FDate (System.DateOnly(2020, 1, 1)))]);
    ("b", FMap [("k", FStr "string")])
]
