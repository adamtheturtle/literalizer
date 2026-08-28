module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RList [)
    dbg (    RInt 1i128,)
    dbg (    RInt 2i128,)
    dbg (    ]))
    dbg (process (RList [)
    dbg (    RInt 3i128,)
    dbg (    ]))
    {}
