module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RDict [("value", RInt 1i128)]))
    dbg (process (RDict [("value", RStr "hello")]))
    {}
