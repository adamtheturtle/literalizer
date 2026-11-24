module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("minimum", FInt(-0o20000000000L));
    ("neighbor", FInt(-0o17777777777L));
    ("maximum", FInt 0o17777777777L);
    ("nested", FList [FInt(-0o20000000000L)])
]
