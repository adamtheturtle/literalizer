module [main]

api_worker_process : a, b -> {}
api_worker_process = \_, _ -> {}

main =
    dbg (api_worker_process (RList [RInt 1i128, RDict []]) (RInt 42i128))
    dbg (api_worker_process (RList [RInt 2i128, RDict [("x", RStr "s")]]) (RInt 43i128))
    {}
