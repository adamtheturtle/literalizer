module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("name", FStr "Alice");
    ("scores", FMap [("1", FStr "first"); ("2", FStr "second")])
]
