process = |_| {}
emit = |_| {}



main! = |_args| {
    dbg (emit(process(RInt(42.I128))))
    Ok({})
}
