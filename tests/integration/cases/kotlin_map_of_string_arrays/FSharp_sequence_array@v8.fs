module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", [|FStr "x"|]);
    ("b", [|FStr "y"|])
]
