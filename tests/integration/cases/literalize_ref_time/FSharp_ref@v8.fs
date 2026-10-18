module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let myTime: Val = FStr (string (System.TimeOnly(1, 2, 3)))
let my_data: Val = FMap [
    ("x", myTime)
]
