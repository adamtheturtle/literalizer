module [main]

process_api_fetch : a -> {}
process_api_fetch = \_ -> {}

main =
    dbg (process_api_fetch (RDict [("data", RStr "hello")]))
    dbg (process_api_fetch (RDict [("data", RInt 42i128)]))
    dbg (process_api_fetch (RDict [("data", RBool Bool.true)]))
    {}
