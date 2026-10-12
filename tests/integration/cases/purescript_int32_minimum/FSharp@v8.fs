module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("minimum", FInt(-2147483648L));
    ("neighbor", FInt(-2147483647L));
    ("maximum", FInt 2147483647L);
    ("nested", FList [FInt(-2147483648L)])
]
