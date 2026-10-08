module Main

type Val =
    | FInt of int64
    | FList of Val list
let emptyValues: Val = FList []
let integerValues: Val = FList [
    FInt 1L
]
let my_data: Val = FList [
    emptyValues;
    integerValues
]
