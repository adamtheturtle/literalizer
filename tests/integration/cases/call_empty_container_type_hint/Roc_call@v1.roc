process = |_, _| {}



main! = |_args| {
    dbg (process(RList([RInt(1.I128), RDict([])]), RInt(42.I128)))
    Ok({})
}
