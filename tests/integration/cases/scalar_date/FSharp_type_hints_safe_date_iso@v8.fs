module Main

type Val =
    | FStr of string
    | FDate of System.DateTime
let my_data: Val = FStr "2024-01-15"
