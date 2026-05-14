module [main]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]
process : a, b -> {}
process = \_, _ -> {}

my_ints : Val
my_ints = RList [
    RInt 1i128,
    RInt 2i128,
    RInt 3i128,
    ]
my_strings : Val
my_strings = RList [
    RStr "a",
    RStr "b",
    ]
my_empty : Val
my_empty = RList []
main =
    dbg (process my_ints (RInt 42i128))
    dbg (process my_strings (RInt 7i128))
    dbg (process my_empty (RInt 99i128))
    {}
