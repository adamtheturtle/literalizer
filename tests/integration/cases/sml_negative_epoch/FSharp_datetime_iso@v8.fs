module Main

type Val =
    | FList of Val list
    | FStr of string
let my_data: Val = FList [
    FStr "1960-01-01T00:00:00+00:00"
]
