Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # before
    ("answer", RInt(42.I128)),  # inline
    ("plain", RStr("ok")),
    # trailing
])

main! = |_args| {
    _ = my_data
    Ok({})
}
