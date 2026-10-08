module [main]

do_thing : a -> {}
do_thing = \_ -> {}

main =
    dbg (do_thing (RInt 1i128))
    dbg (do_thing (RInt 2i128))
    {}
