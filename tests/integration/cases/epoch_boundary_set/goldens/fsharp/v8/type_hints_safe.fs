module Main

type Val =
    | FSet of Val list
    | FDatetime of System.DateTime
let my_data: Val = FSet [
    FDatetime (System.DateTime(1901, 12, 13, 20, 45, 51));
    FDatetime (System.DateTime(1901, 12, 13, 20, 45, 52));
    FDatetime (System.DateTime(2038, 1, 19, 3, 14, 7));
    FDatetime (System.DateTime(2038, 1, 19, 3, 14, 8))
]
