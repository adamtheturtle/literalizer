module [main]

class : a -> {}
class = \_ -> {}

main =
    dbg (class (RInt 42i128))
    {}
