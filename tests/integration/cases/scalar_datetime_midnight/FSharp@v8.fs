module Main

type Val =
    | FStr of string
    | FDatetime of System.DateTime
let my_data: Val = FStr (string (System.DateTime(2024, 1, 15, 0, 0, 0)))
