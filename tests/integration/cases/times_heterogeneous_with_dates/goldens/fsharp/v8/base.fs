module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    | FDate of System.DateOnly
let my_data: Val = FMap [
    ("vals", FList [FDate (System.DateOnly(2024, 1, 15)); FStr (string (System.TimeOnly(9, 30, 0)))])
]
