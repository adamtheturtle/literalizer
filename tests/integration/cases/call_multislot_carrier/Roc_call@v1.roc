process = |_, _| {}



main! = |_args| {
    dbg (process(RInt(1.I128), RStr("hello")))
    dbg (process(RStr("two"), RBool(Bool.False)))
    dbg (process(RFloat(3.5.F64), RNull))
    Ok({})
}
