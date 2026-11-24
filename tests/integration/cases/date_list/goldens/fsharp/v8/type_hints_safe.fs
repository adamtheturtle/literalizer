module Main

type Val =
    | FList of Val list
    | FDate of System.DateOnly
let my_data: Val = FList [
    FDate (System.DateOnly(2024, 1, 15));
    FDate (System.DateOnly(2024, 2, 20))
]
