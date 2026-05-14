module [main]

throttler_check : a, b -> {}
throttler_check = \_, _ -> {}
emit : a -> {}
emit = \_ -> {}

main =
    dbg (emit (throttler_check (RStr "user_1") (RFloat 1000.0)))
    dbg (emit (throttler_check (RStr "user_2") (RFloat 2000.5)))
    {}
