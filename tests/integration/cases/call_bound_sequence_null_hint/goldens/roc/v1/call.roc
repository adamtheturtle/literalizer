Val := [
    RNull,
    RInt(I128),
    RList(List(Val)),
]
consume = |_| {}

item : Val
item = RList([
    RInt(1.I128),
    RInt(2.I128),
])

main! = |_args| {
    dbg (consume(item))
    Ok({})
}
