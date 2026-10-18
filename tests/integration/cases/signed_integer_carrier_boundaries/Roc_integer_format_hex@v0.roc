module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("i32_below", RInt -0x80000001i128),
    ("i32_minimum", RInt -0x80000000i128),
    ("i32_above", RInt -0x7fffffffi128),
    ("i32_maximum", RInt 0x7fffffffi128),
    ("i32_over", RInt 0x80000000i128),
    ("i64_minimum", RInt -0x8000000000000000i128),
    ("i64_maximum", RInt 0x7fffffffffffffffi128),
]
