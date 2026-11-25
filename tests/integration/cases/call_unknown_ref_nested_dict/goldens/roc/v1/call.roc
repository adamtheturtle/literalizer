Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]
process = |_| {}

my_list : Val
my_list = RDict([
    ("unused", RStr("value")),
])

main! = |_args| {
    dbg (process(RList([RList([RDict([("inner", my_list)])])])))
    Ok({})
}
