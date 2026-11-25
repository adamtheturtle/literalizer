Val := [
    RNull,
]
consume = |_| {}

value : Val
value = RNull

main! = |_args| {
    dbg (consume(value))
    Ok({})
}
