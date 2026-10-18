module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let emptyValues: Val = FList []
let integerValues: Val = FList [
    FInt 1L
]
let floatValues: Val = FList [
    FFloat 1.5
]
let my_data: Val = FList [
    emptyValues;
    integerValues;
    floatValues
]
