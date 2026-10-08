module [main]

helper_list : a -> {}
helper_list = \_ -> {}

main =
    dbg (helper_list (RInt 1i128))
    {}
