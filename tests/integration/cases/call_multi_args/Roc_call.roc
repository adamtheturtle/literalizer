module [main]

process : a, b -> {}
process = \_, _ -> {}

main =
    dbg (process (RInt 1i128) (RInt 42i128))
    dbg (process (RInt 2i128) (RInt 100i128))
    {}
