Val := [
    RInt(I128),
    RList(List(Val)),
]
process = |_| {}

unknown_value : Val
unknown_value = RList([
    RInt(1.I128),
])

main! = |_args| {
    dbg (process(unknown_value))
    Ok({})
}
