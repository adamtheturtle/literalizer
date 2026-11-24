process = |_| {}



main! = |_args| {
    dbg (process(RDict([("a", RInt(1.I128)), ("b", RInt(2.I128))])))
    Ok({})
}
