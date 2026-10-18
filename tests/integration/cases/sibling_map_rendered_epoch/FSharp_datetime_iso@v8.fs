module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FMap [("k", FStr "2040-01-01T00:00:00+00:00")]);
    ("b", FMap [("k", FInt 1L)])
]
