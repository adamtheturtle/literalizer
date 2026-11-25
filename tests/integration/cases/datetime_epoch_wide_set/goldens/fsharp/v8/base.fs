module Main

type Val =
    | FSet of Val list
    | FDatetime of System.DateTime
let my_data: Val = FSet [
    FDatetime (System.DateTime(2099, 6, 15, 8, 30, 0))
]
