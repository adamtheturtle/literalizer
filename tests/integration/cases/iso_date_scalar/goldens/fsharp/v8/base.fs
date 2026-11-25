module Main

type Val =
    | FDate of System.DateOnly
let my_data: Val = FDate (System.DateOnly(2000, 1, 1))
