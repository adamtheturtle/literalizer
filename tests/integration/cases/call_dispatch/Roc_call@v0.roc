module [main]

put : a, b -> {}
put = \_, _ -> {}
get : a -> {}
get = \_ -> {}

main =
    dbg (put (RInt 1i128) (RInt 10i128))
    dbg (get (RInt 1i128))
    {}
