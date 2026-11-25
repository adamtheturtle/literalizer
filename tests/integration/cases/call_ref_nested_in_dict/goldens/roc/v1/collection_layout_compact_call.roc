Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]
process = |_| {}

my_var : Val
my_var = RInt(42.I128)

main! = |_args| {
    dbg (process(RDict([("key", my_var), ("count", RInt(42.I128)), ("label", RStr("example"))])))
    Ok({})
}
