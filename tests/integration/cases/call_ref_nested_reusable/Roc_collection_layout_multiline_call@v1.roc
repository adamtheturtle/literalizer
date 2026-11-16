Val := [
    RInt(I128),
    RList(List(Val)),
]
process = |_| {}

item : Val
item = RList([
    RInt(1.I128),
    RInt(2.I128),
])

main! = |_args| {
    dbg (process(RList([
        item,
        item,
    ])))
    Ok({})
}
