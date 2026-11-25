Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RInt(1.I128)),  # tab here and bidi <U+202E>after
    ("b", RInt(2.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
