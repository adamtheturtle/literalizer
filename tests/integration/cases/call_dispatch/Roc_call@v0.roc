module [main]

store_item : a, b -> {}
store_item = \_, _ -> {}
read_item : a -> {}
read_item = \_ -> {}

main =
    dbg (store_item (RInt 1i128) (RInt 10i128))
    dbg (read_item (RInt 1i128))
    {}
