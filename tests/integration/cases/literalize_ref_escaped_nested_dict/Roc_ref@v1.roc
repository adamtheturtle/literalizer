Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

existing : Val
existing = RInt(1.I128)
my_data : Val
my_data = RDict([
    ("nested", RList([RInt(0.I128), existing])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
