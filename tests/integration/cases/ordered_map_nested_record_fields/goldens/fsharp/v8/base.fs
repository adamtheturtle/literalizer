module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("first", FMap [("x", FInt 1L)]);
    ("second", FMap [("y", FInt 2L)])
]
