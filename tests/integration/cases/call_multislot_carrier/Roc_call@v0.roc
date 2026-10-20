module [main]

process : a, b -> {}
process = \_, _ -> {}

main =
    dbg (process (RInt 1i128) (RStr "hello"))
    dbg (process (RStr "two") (RBool Bool.false))
    dbg (process (RFloat 3.5) (RNull))
    {}
