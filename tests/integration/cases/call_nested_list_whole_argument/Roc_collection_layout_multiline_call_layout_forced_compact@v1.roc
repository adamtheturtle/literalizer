f = |_| {}



main! = |_args| {
    dbg (f(RList([RList([RInt(1.I128), RInt(2.I128)]), RList([RInt(3.I128)])])))
    Ok({})
}
