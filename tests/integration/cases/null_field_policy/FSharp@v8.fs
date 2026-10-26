module Main

type Val =
    | FNull
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("drop", FNull);
    ("keep", FInt 1L)
]
