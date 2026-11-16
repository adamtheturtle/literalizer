Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a_b", RInt(0x1.I128)),
    ("a-b", RInt(0x2.I128)),
    ("averyveryverylongkeynamethatgoesonandonandon", RInt(0x3.I128)),
    ("averyveryverylongkeynamethatgoesonandmore", RInt(0x4.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
