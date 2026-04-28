module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a, b -> {}
process = \_, _ -> {}

main =
    _ = my_var : Val
    _ = my_var = RList [
    _ =     RInt 1,
    _ =     RInt 2,
    _ =     RInt 3,
    _ =     ]
    _ = my_other : Val
    _ = my_other = RList [
    _ =     RInt 4,
    _ =     RInt 5,
    _ =     RInt 6,
    _ =     ]
    _ = process my_var (RInt 42)
    _ = process my_other (RInt 7)
    {}
