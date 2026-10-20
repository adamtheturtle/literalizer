module [main]

Val : [
    RNull,
]
consume : a -> {}
consume = \_ -> {}

value : Val
value = RNull
main =
    dbg (consume value)
    {}
