module [main]

op : a -> {}
op = \_ -> {}

main =
    dbg (op (RStr "hello"))
    {}
