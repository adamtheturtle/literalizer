module Main

type Val =
    | JDatetime of System.DateTime
let my_data: Val = JDatetime (System.DateTime(2024, 1, 15, 12, 30, 0))
