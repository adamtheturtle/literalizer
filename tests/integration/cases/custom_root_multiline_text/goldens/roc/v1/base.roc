Val := [
    RStr(Str),
]

custom_data : Val
custom_data = RStr("head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail")

main! = |_args| {
    _ = custom_data
    Ok({})
}
