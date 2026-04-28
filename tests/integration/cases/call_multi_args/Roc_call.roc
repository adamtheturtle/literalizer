module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a, b -> {}
process = \_, _ -> {}

main =
    _ = process (RInt 1) (RInt 42)
    _ = process (RInt 2) (RInt 100)
    {}
