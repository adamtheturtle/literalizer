module [main]

Val : [
    RInt I128,
]
consume : a -> {}
consume = \_ -> {}

shared : Val
shared = RInt 42i128
main =
    dbg (consume shared)
    {}
