module [main]

process : a, b -> {}
process = \_, _ -> {}

main =
    dbg (process (RInt 1i128) (RInt 2i128))
    dbg (process (RInt 3i128) (RInt 4i128))
    {}
