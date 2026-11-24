app_client_fetch = |_| {}



main! = |_args| {
    dbg (app_client_fetch(RStr("hello")))
    dbg (app_client_fetch(RStr("world")))
    Ok({})
}
