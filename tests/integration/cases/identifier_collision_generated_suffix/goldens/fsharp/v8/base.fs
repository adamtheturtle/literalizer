module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a-b", FInt 1L);
    ("a b", FInt 2L);
    ("a-b-2", FInt 3L)
]
