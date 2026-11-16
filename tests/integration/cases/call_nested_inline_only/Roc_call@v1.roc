f = |_, _| {}



main! = |_args| {
    dbg (f(RInt(2.I128), RStr("hello")))  # trailing note
    dbg (f(RInt(3.I128), RStr("world")))  # another note
    Ok({})
}
