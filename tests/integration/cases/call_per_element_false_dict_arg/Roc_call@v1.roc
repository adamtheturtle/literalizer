process = |_| {}



main! = |_args| {
    dbg (process(RDict([("a", RInt(1.I128)), ("b", RStr("x"))])))
    Ok({})
}
