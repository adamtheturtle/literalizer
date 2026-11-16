process = |_| {}
emit = |_, _| {}



main! = |_args| {
    dbg (emit(process(RInt(1.I128)), RStr("2024-01-15")))
    Ok({})
}
