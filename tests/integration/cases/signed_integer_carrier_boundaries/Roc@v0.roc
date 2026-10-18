module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("i32_below", RInt -2147483649i128),
    ("i32_minimum", RInt -2147483648i128),
    ("i32_above", RInt -2147483647i128),
    ("i32_maximum", RInt 2147483647i128),
    ("i32_over", RInt 2147483648i128),
    ("i64_minimum", RInt -9223372036854775808i128),
    ("i64_maximum", RInt 9223372036854775807i128),
]
