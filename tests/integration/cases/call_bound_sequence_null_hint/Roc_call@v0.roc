module [main]

Val : [
    RNull,
    RInt I128,
    RList (List Val),
]
consume : a -> {}
consume = \_ -> {}

item : Val
item = RList [
    RInt 1i128,
    RInt 2i128,
]
main =
    dbg (consume item)
    {}
