process = |_| {}



main! = |_args| {
    dbg (process(RNull))
    dbg (process(RList([RInt(1.I128), RInt(2.I128)])))
    Ok({})
}
