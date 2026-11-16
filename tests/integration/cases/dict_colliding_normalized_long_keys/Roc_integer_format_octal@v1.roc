Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a_b", RInt(0o1.I128)),
    ("a-b", RInt(0o2.I128)),
    ("averyveryverylongkeynamethatgoesonandonandon", RInt(0o3.I128)),
    ("averyveryverylongkeynamethatgoesonandmore", RInt(0o4.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
