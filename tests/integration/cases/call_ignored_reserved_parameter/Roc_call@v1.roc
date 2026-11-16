process = |_| {}



main! = |_args| {
    dbg (process(RInt(42.I128)))
    Ok({})
}
