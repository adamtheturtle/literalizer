module Main

type Val =
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FFloat 1.0e-9;
    FFloat(-1.0e-9)
]
