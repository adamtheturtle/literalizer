module [main]

process : a, b -> {}
process = \_, _ -> {}

main =
    dbg (process (RList [RInt 1i128, RDict []]) (RInt 42i128))
    {}
