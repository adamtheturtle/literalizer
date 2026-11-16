process = |_, _| {}



main! = |_args| {
    dbg (process(RInt(1.I128), RInt(42.I128)))
    dbg (process(RInt(2.I128), RInt(100.I128)))
    Ok({})
}
