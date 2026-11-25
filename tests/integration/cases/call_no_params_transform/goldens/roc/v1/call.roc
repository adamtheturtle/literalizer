process = || {}
emit = |_| {}



main! = |_args| {
    dbg (emit(process()))
    dbg (emit(process()))
    Ok({})
}
