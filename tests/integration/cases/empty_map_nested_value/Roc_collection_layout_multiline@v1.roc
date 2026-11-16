Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RList([
        RDict([
            ("mapping", RDict([])),
        ]),
        RDict([]),
    ]),
    RList([
        RDict([]),
        RDict([
            ("mapping", RDict([])),
        ]),
    ]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
