Val := [
    JInt(I128),
    JStr(Str),
    JDict(List((Str, Val))),
]

my_data : Val
my_data = JDict([
    ("quote\"backslash\\", JInt(1.I128)),
    ("line\nbreak", JInt(2.I128)),
    ("\$(literal)\${text}", JInt(3.I128)),
    ("RStr prefix", JInt(4.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
