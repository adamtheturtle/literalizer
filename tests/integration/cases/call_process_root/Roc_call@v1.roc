process_api_fetch = |_| {}



main! = |_args| {
    dbg (process_api_fetch(RDict([("data", RStr("hello"))])))
    dbg (process_api_fetch(RDict([("data", RInt(42.I128))])))
    dbg (process_api_fetch(RDict([("data", RBool(Bool.True))])))
    Ok({})
}
