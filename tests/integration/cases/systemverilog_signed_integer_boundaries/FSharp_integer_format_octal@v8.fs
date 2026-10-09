module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("i32_below", FInt(-0o20000000001L));
    ("i32_minimum", FInt(-0o20000000000L));
    ("i32_above", FInt(-0o17777777777L));
    ("i32_maximum", FInt 0o17777777777L);
    ("i32_over", FInt 0o20000000000L);
    ("i64_minimum", FInt(-0o1000000000000000000000L));
    ("i64_maximum", FInt 0o777777777777777777777L)
]
