module [main]

f : a -> {}
f = \_ -> {}

main =
    dbg (f (RList []))
    {}
