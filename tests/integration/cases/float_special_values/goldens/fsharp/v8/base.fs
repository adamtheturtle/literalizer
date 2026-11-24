module Main

type Val =
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FFloat infinity;
    FFloat(-infinity);
    FFloat nan
]
