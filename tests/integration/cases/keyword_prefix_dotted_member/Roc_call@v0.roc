module [main]

thing_first_value : a -> {}
thing_first_value = \_ -> {}

main =
    dbg (thing_first_value (RInt 1i128))
    {}
