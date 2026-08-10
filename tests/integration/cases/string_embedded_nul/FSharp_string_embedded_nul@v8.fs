module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("x", FStr "\000");
    ("y", FStr "\0001")
]
