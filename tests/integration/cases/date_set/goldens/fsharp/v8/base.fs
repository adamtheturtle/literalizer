module Main

type Val =
    | FSet of Val list
    | FDate of System.DateOnly
let my_data: Val = FSet [
    FDate (System.DateOnly(2024, 1, 15));
    FDate (System.DateOnly(2024, 6, 1))
]
