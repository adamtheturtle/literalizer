module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FInt 0o1L);
    ("b", FInt 0o20000000000000L)
]
