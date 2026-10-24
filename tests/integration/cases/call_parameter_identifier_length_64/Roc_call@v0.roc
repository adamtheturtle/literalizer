module [main]

f : a -> {}
f = \_ -> {}

main =
    dbg (f (RInt 1i128))
    {}
