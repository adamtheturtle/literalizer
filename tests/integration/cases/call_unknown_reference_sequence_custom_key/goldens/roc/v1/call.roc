Val := [
    RList(List(Val)),
]
process = |_| {}

untyped_value : Val
untyped_value = RList([])

main! = |_args| {
    dbg (process(RList([untyped_value, untyped_value])))
    Ok({})
}
