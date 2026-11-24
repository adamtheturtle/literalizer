module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let shared: Val = FList [
    FInt 1L;
    FStr "x"
]
let my_data: Val = FList [
    shared;
    shared
]
