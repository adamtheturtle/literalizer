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
    dbg (process (RDict [("key", my_var), ("count", RInt 42i128), ("label", RStr "example")]))
    {}
