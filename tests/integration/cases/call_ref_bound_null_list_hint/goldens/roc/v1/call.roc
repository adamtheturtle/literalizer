Val := [
    RNull,
    RInt(I128),
    RList(List(Val)),
]
consume = |_| {}

item : Val
item = RNull

main! = |_args| {
    dbg (consume(item))
    Ok({})
}
