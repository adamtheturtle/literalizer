my_app_http_client_fetch = |_| {}



main! = |_args| {
    dbg (my_app_http_client_fetch(RStr("hello")))
    dbg (my_app_http_client_fetch(RInt(42.I128)))
    dbg (my_app_http_client_fetch(RBool(Bool.True)))
    Ok({})
}
