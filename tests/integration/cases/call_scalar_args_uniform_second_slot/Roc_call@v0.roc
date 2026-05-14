module [main]

process : a, b -> {}
process = \_, _ -> {}

main =
    dbg (process (RStr "hello") (RStr "a"))
    dbg (process (RInt 42i128) (RStr "b"))
    dbg (process (RBool Bool.true) (RStr "c"))
    {}
