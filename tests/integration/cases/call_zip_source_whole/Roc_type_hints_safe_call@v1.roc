process = |_| {}
emit = |_, _| {}



main! = |_args| {
    dbg (emit(process(RInt(42.I128)), RBool(Bool.True)))
    Ok({})
}
