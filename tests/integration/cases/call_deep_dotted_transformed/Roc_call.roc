module [main]

app_client_fetch : a -> {}
app_client_fetch = \_ -> {}
emit : a -> {}
emit = \_ -> {}

main =
    dbg (emit (app_client_fetch (RStr "hello")))
    dbg (emit (app_client_fetch (RInt 42i128)))
    dbg (emit (app_client_fetch (RBool Bool.true)))
    {}
