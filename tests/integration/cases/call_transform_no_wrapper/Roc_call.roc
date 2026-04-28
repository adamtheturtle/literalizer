module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RStr "hello"))
    dbg (process (RInt 42i128))
    dbg (process (RBool Bool.true))
    {}
