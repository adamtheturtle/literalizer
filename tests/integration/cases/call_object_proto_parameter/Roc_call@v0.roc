module [main]

capture : a -> {}
capture = \_ -> {}

main =
    dbg (capture (RInt 1i128))
    {}
