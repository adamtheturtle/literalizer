module Main

type Val =
    | FStr of string
    | FDate of System.DateTime
let mutable my_data: Val = FStr (string (System.DateOnly(2024, 1, 15)))
