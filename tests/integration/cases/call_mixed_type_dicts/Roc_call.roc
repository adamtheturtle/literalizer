module [main]

app_mgr_op : a -> {}
app_mgr_op = \_ -> {}

main =
    dbg (app_mgr_op (RDict [("type", RStr "create"), ("pr_id", RStr "pr_1"), ("draft", RBool Bool.true)]))
    dbg (app_mgr_op (RDict [("type", RStr "create"), ("pr_id", RStr "pr_2")]))
    {}
