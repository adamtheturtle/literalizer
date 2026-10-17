module [main]

make_widget : a -> {}
make_widget = \_ -> {}

main =
    dbg (make_widget (RInt 1i128))
    {}
