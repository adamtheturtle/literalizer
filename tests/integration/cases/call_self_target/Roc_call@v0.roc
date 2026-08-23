module [main]

self : a -> {}
self = \_ -> {}

main =
    dbg (self (RStr "hello"))
    {}
