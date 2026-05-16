module [main]

process : a -> {}
process = \_ -> {}

main =
    dbg (process (RStr "Dune")  # first edition)
    dbg (process (RStr "Solaris"))
    dbg (process (RStr "Neuromancer")  # cyberpunk)
    {}
