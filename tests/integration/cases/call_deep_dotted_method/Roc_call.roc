module [main]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RList (List Val),
]
obj_api_client_post : a -> {}
obj_api_client_post = \_ -> {}

main =
    _ = obj_api_client_post (RStr "hello")
    _ = obj_api_client_post (RInt 42)
    _ = obj_api_client_post (RBool Bool.true)
    {}
