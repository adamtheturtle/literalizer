process = |_| {}



main! = |_args| {
    dbg (process(RList([RInt(1.I128), RStr("x")])))
    Ok({})
}
