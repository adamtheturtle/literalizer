module [main]

f : a -> {}
f = \_ -> {}

main =
    dbg (f (RList [RList [RStr "DEL", RStr "b", RStr "10"], RList [RStr "ADD", RStr "a", RStr "x"]]))  # note
    {}
