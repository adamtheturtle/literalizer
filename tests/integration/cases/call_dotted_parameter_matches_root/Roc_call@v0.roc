module [main]

outer_inner : a, b -> {}
outer_inner = \_, _ -> {}

main =
    dbg (outer_inner (RInt 1i128) (RInt 2i128))
    {}
