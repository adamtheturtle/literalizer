module [main]

Val : [
    RNull,
    RInt I128,
    RList (List Val),
]
consume : a -> {}
consume = \_ -> {}

item : Val
item = RNull
main =
    dbg (consume item)
    {}
