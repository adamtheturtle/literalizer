module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("below", FInt(-0x80000001L));
    ("minimum", FInt(-0x80000000L));
    ("above", FInt(-0x7fffffffL));
    ("nested", FList [FInt 0x0L])
]
