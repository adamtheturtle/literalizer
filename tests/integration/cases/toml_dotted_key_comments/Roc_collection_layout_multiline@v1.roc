Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # first dotted key
    # second dotted key
    ("a", RDict([
        ("b", RInt(1.I128)),
        ("c", RInt(2.I128)),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
