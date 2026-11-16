process = |_| {}



main! = |_args| {
    dbg (process(RNull))
    dbg (process(RStr("hello")))
    Ok({})
}
