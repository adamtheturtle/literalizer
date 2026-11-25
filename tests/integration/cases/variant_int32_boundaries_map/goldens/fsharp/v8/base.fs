module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("below", FInt(-2147483649L));
    ("minimum", FInt(-2147483648L));
    ("above", FInt(-2147483647L));
    ("nested", FList [FInt 0L])
]
