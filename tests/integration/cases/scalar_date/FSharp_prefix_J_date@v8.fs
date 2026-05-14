module Main

type Val =
    | JStr of string
    | JDate of System.DateTime
let my_data: Val = JStr (string (System.DateOnly(2024, 1, 15)))
