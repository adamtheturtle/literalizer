process = |_| {}
emit = |_, _| {}



main! = |_args| {
    dbg (emit(process(RInt(1.I128)), RInt(42.I128)))
    Ok({})
}
