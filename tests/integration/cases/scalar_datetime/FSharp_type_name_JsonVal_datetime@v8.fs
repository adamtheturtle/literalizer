module Main

type JsonVal =
    | FStr of string
    | FDatetime of System.DateTime
let my_data: JsonVal = FStr (string (System.DateTime(2024, 1, 15, 12, 30, 0)))
