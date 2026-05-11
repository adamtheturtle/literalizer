module [main]

process : a, b, c, d -> {}
process = \_, _, _, _ -> {}

main =
    dbg (process (RInt 1i128) (RInt 2i128) (RInt 3i128) (RInt 4i128))
    dbg (process (RInt 10i128) (RInt 20i128) (RInt 30i128) (RInt 40i128))
    {}
