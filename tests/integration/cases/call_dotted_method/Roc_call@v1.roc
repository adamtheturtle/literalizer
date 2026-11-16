app_client_fetch = |_| {}



main! = |_args| {
    dbg (app_client_fetch(RStr("hello")))
    dbg (app_client_fetch(RInt(42.I128)))
    dbg (app_client_fetch(RBool(Bool.True)))
    Ok({})
}
