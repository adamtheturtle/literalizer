process = |_| {}
emit = |_, _| {}



main! = |_args| {
    dbg (emit(process(RStr("hello")), RBool(Bool.True)))
    dbg (emit(process(RInt(42.I128)), RBool(Bool.False)))
    Ok({})
}
