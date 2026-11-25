JsonVal := [
    RInt(I128),
]
process = |_| {}

value : JsonVal
value = RInt(1.I128)

main! = |_args| {
    dbg (process(value))
    Ok({})
}
