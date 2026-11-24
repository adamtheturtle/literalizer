Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("first", RDict([
        ("x", RInt(1.I128)),
        ("y", RInt(2.I128)),
    ])),
    ("second", RDict([
        ("z", RInt(3.I128)),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
