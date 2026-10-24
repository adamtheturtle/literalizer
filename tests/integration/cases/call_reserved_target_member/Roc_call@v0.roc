module [main]

obj_class : a -> {}
obj_class = \_ -> {}

main =
    dbg (obj_class (RInt 42i128))
    {}
