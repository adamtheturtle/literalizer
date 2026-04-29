module [main]

process : a -> {}
process = \_ -> {}
tracer_emit : a -> {}
tracer_emit = \_ -> {}

main =
    dbg (tracer.emit (process (RStr "hello")))
    dbg (tracer.emit (process (RInt 42i128)))
    dbg (tracer.emit (process (RBool Bool.true)))
    {}
