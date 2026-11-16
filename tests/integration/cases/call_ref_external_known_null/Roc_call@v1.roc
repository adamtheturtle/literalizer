Val := [
    RNull,
]
consume = |_| {}

item : Val
item = RNull

main! = |_args| {
    dbg (consume(item))
    Ok({})
}
