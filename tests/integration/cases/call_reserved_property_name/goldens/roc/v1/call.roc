foo_class = |_| {}



main! = |_args| {
    dbg (foo_class(RInt(1.I128)))
    Ok({})
}
