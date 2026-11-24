app_process_fetch = |_| {}



main! = |_args| {
    dbg (app_process_fetch(RDict([("data", RStr("hello"))])))
    dbg (app_process_fetch(RDict([("data", RInt(42.I128))])))
    dbg (app_process_fetch(RDict([("data", RBool(Bool.True))])))
    Ok({})
}
