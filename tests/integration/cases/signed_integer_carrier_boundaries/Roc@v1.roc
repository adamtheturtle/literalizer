Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("i32_below", RInt(-2147483649.I128)),
    ("i32_minimum", RInt(-2147483648.I128)),
    ("i32_above", RInt(-2147483647.I128)),
    ("i32_maximum", RInt(2147483647.I128)),
    ("i32_over", RInt(2147483648.I128)),
    ("i64_minimum", RInt(-9223372036854775808.I128)),
    ("i64_maximum", RInt(9223372036854775807.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
