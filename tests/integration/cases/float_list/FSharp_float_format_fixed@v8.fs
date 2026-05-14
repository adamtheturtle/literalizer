module Main

type Val =
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FFloat 1.100000;
    FFloat(-2.200000);
    FFloat 3.300000
]
