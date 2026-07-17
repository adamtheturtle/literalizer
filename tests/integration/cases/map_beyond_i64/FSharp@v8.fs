module Main

type Val =
    | FInt of bigint
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FInt 9223372036854775807L);
    ("b", FInt 9223372036854775808I)
]
