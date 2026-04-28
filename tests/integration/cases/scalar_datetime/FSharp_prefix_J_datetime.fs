module Main

type Val =
    | JStr of string
    | JDatetime of System.DateTime
let my_data: Val = JStr (string (System.DateTime(2024, 1, 15, 12, 30, 0)))
