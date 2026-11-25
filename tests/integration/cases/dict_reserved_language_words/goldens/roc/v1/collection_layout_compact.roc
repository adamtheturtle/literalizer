Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("assert", RInt(1.I128)),
    ("else", RInt(1.I128)),
    ("error", RInt(1.I128)),
    ("false", RInt(1.I128)),
    ("for", RInt(1.I128)),
    ("function", RInt(1.I128)),
    ("if", RInt(1.I128)),
    ("import", RInt(1.I128)),
    ("importbin", RInt(1.I128)),
    ("importstr", RInt(1.I128)),
    ("in", RInt(1.I128)),
    ("local", RInt(1.I128)),
    ("null", RInt(1.I128)),
    ("self", RInt(1.I128)),
    ("super", RInt(1.I128)),
    ("tailstrict", RInt(1.I128)),
    ("then", RInt(1.I128)),
    ("true", RInt(1.I128)),
    ("ordinary", RInt(1.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
