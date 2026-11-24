module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("minimum", FInt(-0x80000000L));
    ("below", FInt(-0xb2d05e00L))
]
