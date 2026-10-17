module [main]

Val : [
    RInt I128,
    RList (List Val),
]
consume : a -> {}
consume = \_ -> {}

external_value : Val
external_value = RInt 1i128
main =
    dbg (consume external_value)
    {}
