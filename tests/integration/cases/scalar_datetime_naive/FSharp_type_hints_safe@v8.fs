module Main

type Val =
    | FDatetime of System.DateTime
let my_data: Val = FDatetime (System.DateTime(2024, 1, 15, 12, 30, 0))
