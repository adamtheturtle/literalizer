module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let integerValue: Val = FFloat 1.0
let my_data: Val = FList [
    integerValue;
    FFloat 1.5
]
