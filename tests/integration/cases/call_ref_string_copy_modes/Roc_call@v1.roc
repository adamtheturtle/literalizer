Val := [
    RStr(Str),
    RList(List(Val)),
]
consume = |_| {}

item : Val
item = RStr("s")

main! = |_args| {
    dbg (consume(item))
    Ok({})
}
