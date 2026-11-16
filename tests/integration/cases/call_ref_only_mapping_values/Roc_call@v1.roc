Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]
consume = |_| {}

item : Val
item = RInt(42.I128)

main! = |_args| {
    dbg (consume(RDict([("field", item)])))
    Ok({})
}
