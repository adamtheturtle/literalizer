Val := [
    RInt(I128),
]
consume = |_| {}

shared : Val
shared = RInt(42.I128)

main! = |_args| {
    dbg (consume(shared))
    Ok({})
}
