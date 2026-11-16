consume = |_| {}



main! = |_args| {
    dbg (consume(RInt(-2147483649.I128)))
    dbg (consume(RInt(2147483648.I128)))
    Ok({})
}
