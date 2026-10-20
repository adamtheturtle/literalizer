module [main]

Val : [
    RStr Str,
    RList (List Val),
]
consume : a -> {}
consume = \_ -> {}

item : Val
item = RStr "s"
main =
    dbg (consume item)
    {}
