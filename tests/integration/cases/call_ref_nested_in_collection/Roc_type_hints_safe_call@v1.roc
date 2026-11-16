Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]
process = |_, _| {}

big_list : Val
big_list = RList([
    RStr("x"),
])

main! = |_args| {
    dbg (process(RDict([("k", big_list)]), RInt(2.I128)))
    Ok({})
}
