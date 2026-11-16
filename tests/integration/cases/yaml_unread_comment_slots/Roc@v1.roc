Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("flow", RList([
        RInt(1.I128),
        # After the first element.
        RInt(2.I128),
    ])),
    # Between the key and its value.
    ("gap", RInt(3.I128)),
    # On the block scalar header.
    ("block", RStr("Text.\n")),
    ("nested", RList([
        RInt(1.I128),
        RInt(1.I128),
        # On the nested alias.
    ])),
    ("anchored", RInt(4.I128)),
    ("alias", RInt(4.I128)),
    # On the alias.
])

main! = |_args| {
    _ = my_data
    Ok({})
}
