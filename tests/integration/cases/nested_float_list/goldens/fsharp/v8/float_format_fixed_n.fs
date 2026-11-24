module Main

type Val =
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FList [FFloat 1.500000; FFloat 2.500000];
    FList [FFloat 3.500000; FFloat 4.500000]
]
