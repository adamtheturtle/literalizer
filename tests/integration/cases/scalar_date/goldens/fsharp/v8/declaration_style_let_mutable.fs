module Main

type Val =
    | FDate of System.DateOnly
let mutable my_data: Val = FDate (System.DateOnly(2024, 1, 15))
