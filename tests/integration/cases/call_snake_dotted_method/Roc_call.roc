module [main]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RList (List Val),
]
my_app_http_client_fetch : a -> {}
my_app_http_client_fetch = \_ -> {}

main =
    _ = my_app_http_client_fetch (RStr "hello")
    _ = my_app_http_client_fetch (RInt 42)
    _ = my_app_http_client_fetch (RBool Bool.true)
    {}
