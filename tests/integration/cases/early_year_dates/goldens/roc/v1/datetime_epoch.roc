Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("date", RStr("0099-05-27")),
    ("naive", RInt(-62135551800.I128)),
    ("recent", RInt(1716804000.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
