module [main]

api_worker_process : a, b -> {}
api_worker_process = \_, _ -> {}

main =
    dbg (api_worker_process (RDict []) (RDict []))
    {}
