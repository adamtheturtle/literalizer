module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("minimum", FInt(-0b10000000000000000000000000000000L));
    ("neighbor", FInt(-0b1111111111111111111111111111111L));
    ("maximum", FInt 0b1111111111111111111111111111111L);
    ("nested", FList [FInt(-0b10000000000000000000000000000000L)])
]
