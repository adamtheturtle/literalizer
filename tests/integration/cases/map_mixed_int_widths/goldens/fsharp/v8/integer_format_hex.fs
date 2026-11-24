module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FInt 0x1L);
    ("b", FInt 0x10000000000L)
]
