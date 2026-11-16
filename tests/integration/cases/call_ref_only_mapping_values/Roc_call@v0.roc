module [main]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]
consume : a -> {}
consume = \_ -> {}

item : Val
item = RInt 42i128
main =
    dbg (consume (RDict [("field", item)]))
    {}
