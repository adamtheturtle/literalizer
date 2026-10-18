module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("minimum", FInt(-2147483648L));
    ("below", FInt(-3000000000L))
]
