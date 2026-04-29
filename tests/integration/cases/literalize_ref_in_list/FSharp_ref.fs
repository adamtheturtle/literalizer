module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let x: Val = FInt 0L
let y: Val = FInt 0L
let my_data: Val = FList [
    x;
    y
]
