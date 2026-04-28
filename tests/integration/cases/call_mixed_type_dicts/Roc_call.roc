module [main]

Val : [
    RBool Bool,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]
app_mgr_op : a -> {}
app_mgr_op = \_ -> {}

main =
    _ = app_mgr_op (RDict [("type", RStr "create"), ("pr_id", RStr "pr_1"), ("draft", RBool Bool.true)])
    _ = app_mgr_op (RDict [("type", RStr "create"), ("pr_id", RStr "pr_2")])
    {}
