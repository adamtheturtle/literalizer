module [main]

app_mgr_run : a -> {}
app_mgr_run = \_ -> {}

main =
    dbg (app_mgr_run (RDict [("type", RStr "create"), ("pr_id", RStr "pr_1"), ("draft", RBool Bool.true)]))
    dbg (app_mgr_run (RDict [("type", RStr "create"), ("pr_id", RStr "pr_2")]))
    {}
