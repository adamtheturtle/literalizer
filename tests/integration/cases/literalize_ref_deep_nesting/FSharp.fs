module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FMap [("b", FMap [("c", FMap [("$ref", FStr "deep")])])])
]
