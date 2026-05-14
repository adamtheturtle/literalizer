module Main

type Val =
    | FList of Val list
    | FStr of string
    | FDatetime of System.DateTime
let my_data: Val = FList [
    FStr "2024-01-15T12:30:00.123456+00:00";
    FStr "2024-06-01T08:00:00+00:00"
]
