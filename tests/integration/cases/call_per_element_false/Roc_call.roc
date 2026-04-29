module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RInt 1i128))
    {}
