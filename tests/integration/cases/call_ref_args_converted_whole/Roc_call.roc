module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

main =
    _ = my_var : Val
    _ = my_var = RList [
    _ =     RInt 1,
    _ =     RInt 2,
    _ =     RInt 3,
    _ =     ]
    _ = process my_var
    {}
