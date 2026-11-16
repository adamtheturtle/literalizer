process = |_| {}
emit = |_, _| {}



main! = |_args| {
    dbg (emit(process(RInt(1.I128)), RFloat(1.5.F64)))
    Ok({})
}
