Val := [
    RList(List(Val)),
]
process = |_| {}

unknown_value : Val
unknown_value = RList([])

main! = |_args| {
    dbg (process(unknown_value))
    Ok({})
}
