module Main

type JsonVal =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FMap of (string * JsonVal) list
let my_data: JsonVal = FMap [
    ("name", FStr "Alice");
    ("age", FInt 30L);
    ("active", FBool true);
    ("score", FNull)
]
