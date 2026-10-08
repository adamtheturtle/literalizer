module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let floatingValue: Val = FFloat 1.5
let integerValue: Val = FFloat 2.0
let my_data: Val = FList [
    floatingValue;
    integerValue
]
