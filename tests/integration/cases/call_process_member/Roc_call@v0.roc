module [main]

app_process_fetch : a -> {}
app_process_fetch = \_ -> {}

main =
    dbg (app_process_fetch (RDict [("data", RStr "hello")]))
    dbg (app_process_fetch (RDict [("data", RInt 42i128)]))
    dbg (app_process_fetch (RDict [("data", RBool Bool.true)]))
    {}
