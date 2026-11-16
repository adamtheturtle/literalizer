Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("if", RInt(1.I128)),
    ("then", RInt(2.I128)),
    ("else", RInt(3.I128)),
    ("let", RInt(4.I128)),
    ("in", RInt(5.I128)),
    ("using", RInt(6.I128)),
    ("missing", RInt(7.I128)),
    ("assert", RInt(8.I128)),
    ("as", RInt(9.I128)),
    ("Infinity", RInt(10.I128)),
    ("NaN", RInt(11.I128)),
    ("merge", RInt(12.I128)),
    ("Some", RInt(13.I128)),
    ("toMap", RInt(14.I128)),
    ("forall", RInt(15.I128)),
    ("with", RInt(16.I128)),
    ("ordinary", RInt(17.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
