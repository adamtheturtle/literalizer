module Main

type Val =
    | FStr of string
    | FDatetime of System.DateTime
let mutable my_data: Val = FStr (string (System.DateTime(2024, 1, 15, 12, 30, 0)))
