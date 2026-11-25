module Main

type Val =
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FFloat 0.000000001;
    FFloat(-0.000000001)
]
