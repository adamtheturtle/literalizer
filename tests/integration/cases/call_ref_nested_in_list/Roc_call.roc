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
my_other : Val
my_other = RInt 7i128
main =
    dbg (process (RList [my_var, RInt 42i128, RStr "static"]))
    dbg (process (RList [my_other, RInt 7i128, RStr "label"]))
    {}
