module [main]

first_value : a -> {}
first_value = \_ -> {}

main =
    dbg (first_value (RInt 1i128))
    {}
