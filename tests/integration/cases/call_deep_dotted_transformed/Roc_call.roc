module [main]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RList (List Val),
]
app_client_fetch : a -> {}
app_client_fetch = \_ -> {}
emit : a -> {}
emit = \_ -> {}

main =
    _ = emit "$(app_client_fetch (RStr "hello"))"
    _ = emit "$(app_client_fetch (RInt 42))"
    _ = emit "$(app_client_fetch (RBool Bool.true))"
    {}
