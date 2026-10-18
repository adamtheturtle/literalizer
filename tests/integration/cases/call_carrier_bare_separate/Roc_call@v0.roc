module [main]

make_widget : a, b -> {}
make_widget = \_, _ -> {}

main =
    dbg (make_widget (RList [RInt 1i128]) (RList [RStr "text"]))
    {}
