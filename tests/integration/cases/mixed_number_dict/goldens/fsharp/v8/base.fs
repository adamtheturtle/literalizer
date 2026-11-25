module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FInt 1L);
    ("b", FFloat 2.5);
    ("c", FInt 3L)
]
