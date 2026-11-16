Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RList([
        RInt(1.I128),
        RInt(2.I128),
        RInt(3.I128),
    ])),  # inline a
    ("b", RInt(2.I128)),  # inline b
])

main! = |_args| {
    _ = my_data
    Ok({})
}
