process = |_| {}



main! = |_args| {
    dbg (process(RStr("a\"b")))
    Ok({})
}
