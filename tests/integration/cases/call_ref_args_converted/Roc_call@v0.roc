module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a, b -> {}
process = \_, _ -> {}

my_var : Val
my_var = RList [
    RInt 1i128,
    RInt 2i128,
    RInt 3i128,
    ]
my_other : Val
my_other = RList [
    RInt 4i128,
    RInt 5i128,
    RInt 6i128,
    ]
main =
    dbg (process my_var (RInt 42i128))
    dbg (process my_other (RInt 7i128))
    {}
