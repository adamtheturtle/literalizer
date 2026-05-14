module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RDict [("a", RInt 1i128), ("b", RInt 2i128)]))
    {}
