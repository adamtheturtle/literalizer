module [main]

consume : a -> {}
consume = \_ -> {}

main =
    dbg (consume (RInt -2147483649i128))
    dbg (consume (RInt 2147483648i128))
    {}
