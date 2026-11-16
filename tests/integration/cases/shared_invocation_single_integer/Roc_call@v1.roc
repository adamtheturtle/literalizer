consume = |_| {}



main! = |_args| {
    dbg (consume(RInt(1.I128)))
    Ok({})
}
