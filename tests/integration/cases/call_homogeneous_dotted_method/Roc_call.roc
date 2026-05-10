module [main]

app_client_fetch : a -> {}
app_client_fetch = \_ -> {}

main =
    dbg (app_client_fetch (RStr "hello"))
    dbg (app_client_fetch (RStr "world"))
    {}
