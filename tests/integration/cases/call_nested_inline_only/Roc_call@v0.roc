module [main]

f : a, b -> {}
f = \_, _ -> {}

main =
    dbg (f (RInt 2i128) (RStr "hello"))  # trailing note
    dbg (f (RInt 3i128) (RStr "world"))  # another note
    {}
