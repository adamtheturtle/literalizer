module Main

type Val =
    | FDate of System.DateOnly
let my_data: Val = FDate (System.DateOnly(2024, 1, 15))
