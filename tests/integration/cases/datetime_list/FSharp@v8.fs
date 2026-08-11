module Main

type Val =
    | FList of Val list
    | FDatetime of System.DateTime
let my_data: Val = FList [
    FDatetime (System.DateTime(2024, 1, 15, 12, 30, 0));
    FDatetime (System.DateTime(2024, 6, 1, 8, 0, 0))
]
