module [main]

Val : [
    RFloat F64,
    RStr Str,
    RList (List Val),
]
throttler_check : a, b -> {}
throttler_check = \_, _ -> {}
emit : a -> {}
emit = \_ -> {}

main =
    _ = emit "$(throttler_check (RStr "user_1") (RFloat 1000.0))"
    _ = emit "$(throttler_check (RStr "user_2") (RFloat 2000.5))"
    {}
