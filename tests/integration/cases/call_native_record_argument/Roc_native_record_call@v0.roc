module [main]

consume : a -> {}
consume = \_ -> {}

main =
    dbg (consume ({ x: 1i128 }))
    {}
