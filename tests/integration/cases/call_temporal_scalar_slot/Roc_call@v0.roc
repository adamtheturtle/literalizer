module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RStr "09:30:00"))
    dbg (process (RStr "2024-01-15T00:00:00+00:00"))
    dbg (process (RInt 1i128))
    {}
