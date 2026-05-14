module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("first", FStr "one");
    ("second", FStr "two");
    ("third", FStr "three")
]
