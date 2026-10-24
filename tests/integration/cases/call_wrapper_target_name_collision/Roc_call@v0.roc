module [main]

check : a -> {}
check = \_ -> {}

main =
    dbg (check (RInt 42i128))
    {}
