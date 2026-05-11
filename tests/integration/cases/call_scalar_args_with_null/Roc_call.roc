module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RNull))
    dbg (process (RStr "hello"))
    {}
