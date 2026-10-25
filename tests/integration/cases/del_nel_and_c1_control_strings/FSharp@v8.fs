module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("del", FStr "ab");
    ("nel", FStr "ab");
    ("c1", FStr "ab")
]
