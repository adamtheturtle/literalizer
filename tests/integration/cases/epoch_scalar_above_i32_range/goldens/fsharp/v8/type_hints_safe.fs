module Main

type Val =
    | FDatetime of System.DateTime
let my_data: Val = FDatetime (System.DateTime(2099, 6, 15, 8, 30, 0))
