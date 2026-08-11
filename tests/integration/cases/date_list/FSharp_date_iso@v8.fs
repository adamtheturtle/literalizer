module Main

type Val =
    | FList of Val list
    | FStr of string
let my_data: Val = FList [
    FStr "2024-01-15";
    FStr "2024-02-20"
]
