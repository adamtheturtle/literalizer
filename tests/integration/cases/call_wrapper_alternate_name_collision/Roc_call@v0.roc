module [main]

check_wrapper : a -> {}
check_wrapper = \_ -> {}

main =
    dbg (check_wrapper (RInt 42i128))
    {}
