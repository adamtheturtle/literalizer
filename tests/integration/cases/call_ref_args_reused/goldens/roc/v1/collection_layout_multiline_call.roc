Val := [
    RInt(I128),
    RList(List(Val)),
]
process = |_, _| {}

single_var : Val
single_var = RList([
    RInt(4.I128),
    RInt(5.I128),
    RInt(6.I128),
])
repeated_var : Val
repeated_var = RInt(1.I128)

main! = |_args| {
    dbg (process(repeated_var, RInt(1.I128)))
    dbg (process(single_var, RInt(0.I128)))
    dbg (process(repeated_var, RInt(8.I128)))
    Ok({})
}
