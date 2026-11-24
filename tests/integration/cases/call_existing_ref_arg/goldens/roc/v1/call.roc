Val := [
    RInt(I128),
    RList(List(Val)),
]
process = |_| {}

existing : Val
existing = RInt(42.I128)

main! = |_args| {
    dbg (process(existing))
    Ok({})
}
