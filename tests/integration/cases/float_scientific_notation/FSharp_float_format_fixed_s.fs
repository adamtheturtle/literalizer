module Main

type Val =
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FFloat 0.000000;
    FFloat 1.000000;
    FFloat 1500.000000;
    FFloat 0.001000
]
