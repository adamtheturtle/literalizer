module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let deep: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = FMap [
    ("a", FMap [("b", FMap [("c", deep)])])
]
