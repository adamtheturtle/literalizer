module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("id", FInt 1L);
    ("owner", FMap [("name", FStr "Alice"); ("age", FInt 30L)])
]
