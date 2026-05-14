module [main]

process : a, b, c, d -> {}
process = \_, _, _, _ -> {}

main =
    dbg (process (RInt 1i128) (RInt 2i128) (RInt 3i128) (RInt 4i128))
    dbg (process (RInt 5i128) (RInt 6i128) (RInt 7i128) (RInt 8i128))
    {}
