module Main

type Val =
    | FStr of string
    | FDatetime of System.DateTime
let my_data: Val = FStr "2024-01-15T18:00:00+05:30"
