check = |_| {}



main! = |_args| {
    dbg (check(RInt(42.I128)))
    Ok({})
}
