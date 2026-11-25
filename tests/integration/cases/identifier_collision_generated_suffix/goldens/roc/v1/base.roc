Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a-b", RInt(1.I128)),
    ("a b", RInt(2.I128)),
    ("a-b-2", RInt(3.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
