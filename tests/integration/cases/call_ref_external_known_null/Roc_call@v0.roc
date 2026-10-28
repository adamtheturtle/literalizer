module [main]

Val : [
    RNull,
]
consume : a -> {}
consume = \_ -> {}

item : Val
item = RNull
main =
    dbg (consume item)
    {}
