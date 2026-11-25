process = |_| {}



main! = |_args| {
    dbg (process(RList([
        RInt(1.I128),
        RInt(2.I128),
    ])))
    dbg (process(RList([
        RInt(3.I128),
    ])))
    Ok({})
}
