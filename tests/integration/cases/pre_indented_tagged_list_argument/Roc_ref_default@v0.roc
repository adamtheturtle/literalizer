module [main]

consume_widget : a -> {}
consume_widget = \_ -> {}

main =
    dbg (consume_widget (    RList [
            RInt 1i128,
            RInt 2i128,
        ]))
    {}
