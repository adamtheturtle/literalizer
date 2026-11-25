process = |_, _| {}



main! = |_args| {
    dbg (process(RInt(1.I128), RInt(2.I128)))
    dbg (process(RInt(3.I128), RInt(4.I128)))
    Ok({})
}
