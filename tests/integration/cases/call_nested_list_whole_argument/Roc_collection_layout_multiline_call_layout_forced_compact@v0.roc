module [main]

f : a -> {}
f = \_ -> {}

main =
    dbg (f (RList [RList [RInt 1i128, RInt 2i128], RList [RInt 3i128]]))
    {}
