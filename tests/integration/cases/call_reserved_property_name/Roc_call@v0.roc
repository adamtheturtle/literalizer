module [main]

foo_class : a -> {}
foo_class = \_ -> {}

main =
    dbg (foo_class (RInt 1i128))
    {}
