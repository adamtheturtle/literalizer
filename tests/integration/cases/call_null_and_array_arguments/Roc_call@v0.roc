module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RNull))
    dbg (process (RList [RInt 1i128, RInt 2i128]))
    {}
