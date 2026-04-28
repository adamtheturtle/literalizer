module [main]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

main =
    _ = process (RStr "hello")
    _ = process (RInt 42)
    _ = process (RBool Bool.true)
    {}
