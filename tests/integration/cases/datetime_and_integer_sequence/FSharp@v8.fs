module Main

type Val =
    | FInt of int64
    | FList of Val list
    | FDatetime of System.DateTime
let my_data: Val = FList [
    FDatetime (System.DateTime(2000, 1, 1, 1, 2, 3));
    FInt 1L
]
