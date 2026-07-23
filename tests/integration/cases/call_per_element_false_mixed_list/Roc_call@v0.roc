module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RList [RInt 1i128, RStr "x"]))
    {}
