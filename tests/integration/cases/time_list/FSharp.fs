open System
module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("times", FList [TimeOnly(9, 30, 0); TimeOnly(17, 45, 0); TimeOnly(23, 59, 59)])
]
