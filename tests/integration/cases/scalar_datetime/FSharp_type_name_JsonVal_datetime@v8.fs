module Main

type JsonVal =
    | FDatetime of System.DateTime
let my_data: JsonVal = FDatetime (System.DateTime(2024, 1, 15, 12, 30, 0))
