module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RInt -1i128))
    dbg (process (RInt -2i128))
    dbg (process (RInt -3i128))
    {}
