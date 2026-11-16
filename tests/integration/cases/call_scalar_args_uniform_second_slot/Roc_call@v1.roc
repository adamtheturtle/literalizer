process = |_, _| {}



main! = |_args| {
    dbg (process(RStr("hello"), RStr("a")))
    dbg (process(RInt(42.I128), RStr("b")))
    dbg (process(RBool(Bool.True), RStr("c")))
    Ok({})
}
