module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FInt of int64
let my_data: Val = FMap [
    ("within_i32", FInt 1705320000L);
    ("beyond_i32", FInt 4085195400L)
]
