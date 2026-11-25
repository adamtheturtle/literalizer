module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let mutable my_data: Val = FMap [
    ("a", FInt 1L);
    ("b", FInt 1099511627776L)
]
