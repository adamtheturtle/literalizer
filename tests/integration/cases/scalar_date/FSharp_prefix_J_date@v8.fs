module Main

type Val =
    | JDate of System.DateOnly
let my_data: Val = JDate (System.DateOnly(2024, 1, 15))
