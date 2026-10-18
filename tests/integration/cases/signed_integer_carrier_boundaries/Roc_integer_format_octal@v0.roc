module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("i32_below", RInt -0o20000000001i128),
    ("i32_minimum", RInt -0o20000000000i128),
    ("i32_above", RInt -0o17777777777i128),
    ("i32_maximum", RInt 0o17777777777i128),
    ("i32_over", RInt 0o20000000000i128),
    ("i64_minimum", RInt -0o1000000000000000000000i128),
    ("i64_maximum", RInt 0o777777777777777777777i128),
]
