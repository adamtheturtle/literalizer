f = |_| {}



main! = |_args| {
    dbg (f(RList([RInt(1.I128), RInt(2.I128)])))
    Ok({})
}
