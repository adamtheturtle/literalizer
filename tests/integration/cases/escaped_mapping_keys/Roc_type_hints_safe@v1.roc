Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("quote\"backslash\\", RInt(1.I128)),
    ("line\nbreak", RInt(2.I128)),
    ("\$(literal)\${text}", RInt(3.I128)),
    ("RStr prefix", RInt(4.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
