module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RInt 42i128))
    {}
