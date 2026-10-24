module Main

type Val =
    | FFloat of float
    | FStr of string
    | FMap of (string * Val) list
let std: Val = FMap [
    ("nan", FFloat nan);
    ("positive", FFloat infinity);
    ("negative", FFloat(-infinity))
]
