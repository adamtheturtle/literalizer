process = |_| {}



main! = |_args| {
    dbg (process(RDict([("value", RInt(1.I128))])))
    dbg (process(RDict([("value", RStr("hello"))])))
    Ok({})
}
