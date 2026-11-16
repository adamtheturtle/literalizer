Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]
process = |_| {}

big_list : Val
big_list = RList([
    RStr("x"),
])

main! = |_args| {
    dbg (process(RDict([("m", big_list)])))
    Ok({})
}
