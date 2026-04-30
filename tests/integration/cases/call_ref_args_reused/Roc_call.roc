module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a, b -> {}
process = \_, _ -> {}

repeated_var : Val
repeated_var = RInt 1i128
single_var : Val
single_var = RList [
    RInt 4i128,
    RInt 5i128,
    RInt 6i128,
    ]
main =
    dbg (process repeated_var (RInt 1i128))
    dbg (process single_var (RInt 0i128))
    dbg (process repeated_var (RInt 8i128))
    {}
