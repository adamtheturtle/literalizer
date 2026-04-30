module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RStr "a\"b"))
    {}
