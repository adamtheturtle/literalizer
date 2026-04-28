module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("1", FStr "one");
    ("2", FStr "two");
    ("42", FStr "answer")
]
