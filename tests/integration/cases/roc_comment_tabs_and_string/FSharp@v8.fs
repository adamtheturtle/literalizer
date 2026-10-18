module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // before	line
    ("value", FStr "left\tright")  // inline	line
    // after	line
]
