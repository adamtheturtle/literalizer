module [main]

app_client_fetch : a -> {}
app_client_fetch = \_ -> {}

main =
    dbg (app_client_fetch (RStr "hello"))
    dbg (app_client_fetch (RInt 42i128))
    dbg (app_client_fetch (RBool Bool.true))
    {}
