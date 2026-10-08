module [main]

f : a, b -> {}
f = \_, _ -> {}

main =
    dbg (f (RInt 1i128) (RInt 2i128))
    {}
