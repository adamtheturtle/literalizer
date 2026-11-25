process = |_| {}



main! = |_args| {
    dbg (process(RStr("hello")))
    dbg (process(RInt(42.I128)))
    dbg (process(RBool(Bool.True)))
    dbg (process(RNull))
    Ok({})
}
