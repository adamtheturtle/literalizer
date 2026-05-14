module [main]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

my_var : Val
my_var = RInt 42i128
main =
    dbg (process (RList [my_var, RInt 42i128, RStr "static"]))
    {}
