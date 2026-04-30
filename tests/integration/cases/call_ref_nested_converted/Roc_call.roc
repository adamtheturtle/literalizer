module [main]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]
process : a -> {}
process = \_ -> {}

my_var : Val
my_var = RInt 42i128
main =
    dbg (process (RList [RDict [("ref", RStr "myVar")], RInt 42i128, RStr "static"]))
    {}
