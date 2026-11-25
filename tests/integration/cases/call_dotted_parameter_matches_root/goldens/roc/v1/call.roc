outer_inner = |_, _| {}



main! = |_args| {
    dbg (outer_inner(RInt(1.I128), RInt(2.I128)))
    Ok({})
}
