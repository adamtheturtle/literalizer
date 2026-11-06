module [main]

consume : a -> {}
consume = \_ -> {}

main =
    dbg (consume (RInt 1i128))
    {}
