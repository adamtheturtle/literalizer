module Main

type Val =
    | FSet of Val list
    | FStr of string
let my_data: Val = FSet [
    FStr "2024-01-15";
    FStr "2024-06-01"
]
