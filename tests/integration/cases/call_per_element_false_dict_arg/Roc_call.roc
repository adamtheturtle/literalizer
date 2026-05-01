module [main]

send : a -> {}
send = \_ -> {}

main =
    dbg (send (RDict [("a", RInt 1i128), ("b", RStr "x")]))
    {}
