Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a-b", RInt(1.I128)),
    ("two words", RInt(2.I128)),
    ("she said \"hi\"", RInt(3.I128)),
    ("", RInt(4.I128)),
    ("valid_key", RInt(5.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
