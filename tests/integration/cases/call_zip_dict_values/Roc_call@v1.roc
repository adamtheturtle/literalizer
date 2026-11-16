process = |_| {}
emit = |_, _| {}



main! = |_args| {
    dbg (emit(process(RStr("hello")), RDict([("a", RInt(1.I128)), ("b", RInt(2.I128))])))
    dbg (emit(process(RInt(42.I128)), RDict([("c", RInt(3.I128)), ("d", RInt(4.I128))])))
    Ok({})
}
