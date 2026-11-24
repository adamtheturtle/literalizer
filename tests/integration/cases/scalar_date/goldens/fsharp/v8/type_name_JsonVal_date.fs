module Main

type JsonVal =
    | FDate of System.DateOnly
let my_data: JsonVal = FDate (System.DateOnly(2024, 1, 15))
