module Main

type Val =
    | FDatetime of System.DateTime
let my_data: Val = FDatetime (System.DateTime(1901, 12, 13, 20, 45, 51))
