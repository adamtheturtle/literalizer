module [main]

obj_api_client_post : a -> {}
obj_api_client_post = \_ -> {}

main =
    dbg (obj_api_client_post (RStr "hello"))
    dbg (obj_api_client_post (RInt 42i128))
    dbg (obj_api_client_post (RBool Bool.true))
    {}
