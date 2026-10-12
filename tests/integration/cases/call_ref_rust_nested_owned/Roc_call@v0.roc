module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

item : Val
item = RList [
    RInt 1i128,
    RInt 2i128,
]
main =
    dbg (process (RList [item, item]))
    {}
