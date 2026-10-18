module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("minimum", FInt(-0b10000000000000000000000000000000L));
    ("below", FInt(-0b10110010110100000101111000000000L))
]
