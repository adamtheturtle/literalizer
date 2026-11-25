module Main

type Val =
    | FNull
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // comment
    ("name", FStr "Alice");
    ("score", FNull)
]
