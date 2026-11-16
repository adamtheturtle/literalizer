Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("i32_below", RInt(-0o20000000001.I128)),
    ("i32_minimum", RInt(-0o20000000000.I128)),
    ("i32_above", RInt(-0o17777777777.I128)),
    ("i32_maximum", RInt(0o17777777777.I128)),
    ("i32_over", RInt(0o20000000000.I128)),
    ("i64_minimum", RInt(-0o1000000000000000000000.I128)),
    ("i64_maximum", RInt(0o777777777777777777777.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
