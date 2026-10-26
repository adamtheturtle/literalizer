module [main]

api_process : a -> {}
api_process = \_ -> {}

main =
    dbg (api_process (RDict []))
    {}
