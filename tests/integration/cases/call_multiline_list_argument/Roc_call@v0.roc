module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RList [
        RInt 1i128,
        RInt 2i128,
        ]))
    dbg (process (RList [
        RInt 3i128,
        ]))
    {}
