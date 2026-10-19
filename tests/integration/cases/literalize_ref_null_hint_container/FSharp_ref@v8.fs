module Main

type Val =
    | FNull
    | FInt of int64
    | FList of Val list
let myValue: Val = FList [
    FInt 1L;
    FInt 2L
]
let my_data: Val = myValue
