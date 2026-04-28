module [main]

my_app_http_client_fetch : a -> {}
my_app_http_client_fetch = \_ -> {}

main =
    dbg (my_app_http_client_fetch (RStr "hello"))
    dbg (my_app_http_client_fetch (RInt 42i128))
    dbg (my_app_http_client_fetch (RBool Bool.true))
    {}
