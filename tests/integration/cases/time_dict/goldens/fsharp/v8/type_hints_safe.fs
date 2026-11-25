module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("morning", FStr (string (System.TimeOnly(9, 30, 0))));
    ("afternoon", FStr (string (System.TimeOnly(14, 15, 0))));
    ("evening", FStr (string (System.TimeOnly(23, 59, 59))))
]
