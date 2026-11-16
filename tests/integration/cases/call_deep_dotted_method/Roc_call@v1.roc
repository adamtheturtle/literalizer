obj_api_client_post = |_| {}



main! = |_args| {
    dbg (obj_api_client_post(RStr("hello")))
    dbg (obj_api_client_post(RInt(42.I128)))
    dbg (obj_api_client_post(RBool(Bool.True)))
    Ok({})
}
