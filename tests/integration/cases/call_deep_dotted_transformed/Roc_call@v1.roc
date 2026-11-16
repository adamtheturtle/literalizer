app_client_fetch = |_| {}
emit = |_| {}



main! = |_args| {
    dbg (emit(app_client_fetch(RStr("hello"))))
    dbg (emit(app_client_fetch(RInt(42.I128))))
    dbg (emit(app_client_fetch(RBool(Bool.True))))
    Ok({})
}
