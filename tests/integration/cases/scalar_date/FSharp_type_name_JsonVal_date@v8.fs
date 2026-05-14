module Main

type JsonVal =
    | FStr of string
    | FDate of System.DateTime
let my_data: JsonVal = FStr (string (System.DateOnly(2024, 1, 15)))
