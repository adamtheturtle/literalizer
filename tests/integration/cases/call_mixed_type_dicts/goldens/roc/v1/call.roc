app_mgr_run = |_| {}



main! = |_args| {
    dbg (app_mgr_run(RDict([("type", RStr("create")), ("pr_id", RStr("pr_1")), ("draft", RBool(Bool.True))])))
    dbg (app_mgr_run(RDict([("type", RStr("create")), ("pr_id", RStr("pr_2"))])))
    Ok({})
}
