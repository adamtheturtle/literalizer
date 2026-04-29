module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (# Test cases)
    dbg (process (RStr "hello")  # single word)
    dbg (process (RStr "hello world")  # two words)
    dbg (# trailing comment)
    {}
