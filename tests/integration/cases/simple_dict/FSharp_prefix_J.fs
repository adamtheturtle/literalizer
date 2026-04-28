module Main

type Val =
    | JNull
    | JBool of bool
    | JInt of int64
    | JStr of string
    | JMap of (string * Val) list
let my_data: Val = JMap [
    ("name", JStr "Alice");
    ("age", JInt 30L);
    ("active", JBool true);
    ("score", JNull)
]
