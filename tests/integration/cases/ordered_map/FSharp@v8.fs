module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("name", FStr "Alice");
    ("age", FInt 30L);
    ("active", FBool true)
]
