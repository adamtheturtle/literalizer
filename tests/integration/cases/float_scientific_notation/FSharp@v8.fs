module Main

type Val =
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FFloat 0.0;
    FFloat 1.0;
    FFloat 1500.0;
    FFloat 0.001;
    FFloat 1e16
]
