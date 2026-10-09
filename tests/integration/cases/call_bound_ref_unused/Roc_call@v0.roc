module [main]

f : a -> {}
f = \_ -> {}

main =
    dbg (f (RList [RInt 1i128, RInt 2i128]))
    {}
