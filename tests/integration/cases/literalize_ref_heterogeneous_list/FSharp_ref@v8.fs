module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let one: Val = FInt 1L
let two: Val = FStr "s"
let my_data: Val = FList [
    one;
    two
]
