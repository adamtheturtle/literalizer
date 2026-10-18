module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("i32_below", FInt(-0x80000001L));
    ("i32_minimum", FInt(-0x80000000L));
    ("i32_above", FInt(-0x7fffffffL));
    ("i32_maximum", FInt 0x7fffffffL);
    ("i32_over", FInt 0x80000000L);
    ("i64_minimum", FInt(-0x8000000000000000L));
    ("i64_maximum", FInt 0x7fffffffffffffffL)
]
