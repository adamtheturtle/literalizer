Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a_b", RInt(0b1.I128)),
    ("a-b", RInt(0b10.I128)),
    ("averyveryverylongkeynamethatgoesonandonandon", RInt(0b11.I128)),
    ("averyveryverylongkeynamethatgoesonandmore", RInt(0b100.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
