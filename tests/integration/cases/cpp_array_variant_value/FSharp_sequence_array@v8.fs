module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FInt 1L);
    ("b", FStr "x");
    ("e", FList ([|FInt 1L; FInt 2L|]));
    ("f", FMap [("g", FStr "h")])
]
