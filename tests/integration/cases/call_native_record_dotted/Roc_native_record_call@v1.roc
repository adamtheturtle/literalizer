app_client_consume = |_, _| {}



main! = |_args| {
    dbg (app_client_consume({ x: 1.I128 }, 2.I128))
    dbg (app_client_consume({ name: "Ada" }, 3.I128))
    Ok({})
}
