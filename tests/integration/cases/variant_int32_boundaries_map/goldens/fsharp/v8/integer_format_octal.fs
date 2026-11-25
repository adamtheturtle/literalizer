module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("below", FInt(-0o20000000001L));
    ("minimum", FInt(-0o20000000000L));
    ("above", FInt(-0o17777777777L));
    ("nested", FList [FInt 0o0L])
]
