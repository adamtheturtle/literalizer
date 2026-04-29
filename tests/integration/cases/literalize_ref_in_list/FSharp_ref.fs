module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let valX: Val = FMap [
    ("_", FStr "_")
]
let valY: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = FList [
    valX;
    valY
]
