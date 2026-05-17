module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("mixed", FList [FList [FStr (string (System.TimeOnly(9, 30, 0)))]; FList []])
]
