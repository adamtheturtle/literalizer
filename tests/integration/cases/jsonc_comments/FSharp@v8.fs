module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("url", FStr "https://example.org/a/*b*/");
    ("count", FInt 2L)
]
