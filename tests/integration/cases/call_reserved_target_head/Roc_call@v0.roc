module [main]

class_member : a -> {}
class_member = \_ -> {}

main =
    dbg (class_member (RInt 42i128))
    {}
