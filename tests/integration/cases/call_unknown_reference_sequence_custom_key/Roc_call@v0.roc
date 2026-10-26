module [main]

Val : [
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

untyped_value : Val
untyped_value = RList []
main =
    dbg (process (RList [untyped_value, untyped_value]))
    {}
