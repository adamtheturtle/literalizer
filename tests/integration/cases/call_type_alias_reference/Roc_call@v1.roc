Val := [
    RInt(I128),
]
process = |_| {}

value : Val
value = RInt(1.I128)

main! = |_args| {
    dbg (process(value))
    Ok({})
}
