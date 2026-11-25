module Main

type Val =
    | FInt of int64
    | FBigInt of bigint
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FInt 9223372036854775807L);
    ("b", FBigInt 9223372036854775808I)
]
