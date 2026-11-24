Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RDict([
        ("b", RList([RInt(1.I128)])),
        # Outdented from the sequence, so the inner mapping claims this.
        ("c", RInt(2.I128)),
    ])),
    # Outdented from the inner mapping too, so the root claims this.
    ("d", RInt(3.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
