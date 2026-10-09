module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("i32_below", FInt(-2147483649L));
    ("i32_minimum", FInt(-2147483648L));
    ("i32_above", FInt(-2147483647L));
    ("i32_maximum", FInt 2147483647L);
    ("i32_over", FInt 2147483648L);
    ("i64_minimum", FInt(-9223372036854775808L));
    ("i64_maximum", FInt 9223372036854775807L)
]
