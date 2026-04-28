module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

my_var : Val
my_var = RList [
    RInt 1i128,
    RInt 2i128,
    RInt 3i128,
    ]
main =
    dbg (process my_var)
    {}
