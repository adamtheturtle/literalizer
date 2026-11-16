Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("numbers", RList([RInt(1.I128), RInt(2.I128)])),
    ("nested", RDict([("inner", RList([RInt(3.I128)]))])),
    ("mixed", RList([RInt(4.I128), RStr("five")])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
