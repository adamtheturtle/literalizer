Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("items", RList([RDict([("inner", RDict([("x", RInt(1.I128))]))]), RDict([("inner", RDict([]))])]))]),
    RDict([("items", RList([RDict([("inner", RDict([("x", RInt(2.I128))]))]), RDict([("inner", RDict([]))])]))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
