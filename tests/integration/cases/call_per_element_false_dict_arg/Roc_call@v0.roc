module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RDict [("a", RInt 1i128), ("b", RStr "x")]))
    {}
