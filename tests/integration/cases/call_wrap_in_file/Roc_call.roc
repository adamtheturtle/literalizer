module [main]

process : a, b -> {}
process = \_, _ -> {}
Val : [
    RInt I128,
    RList (List Val),
]

main =
    _ = process (RInt 1) (RInt 2)
    _ = process (RInt 3) (RInt 4)
    {}
