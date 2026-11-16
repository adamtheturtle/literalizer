Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

        shared : Val
        shared = RList([
            RInt(1.I128),
            RInt(2.I128),
        ])
        my_data : Val
        my_data = RList([
            # A leading comment with { braces, "quotes", and // markers
            RStr("first\n{ \"quoted\" // text }"),
            shared,
        ])

main! = |_args| {
    _ = my_data
    Ok({})
}
