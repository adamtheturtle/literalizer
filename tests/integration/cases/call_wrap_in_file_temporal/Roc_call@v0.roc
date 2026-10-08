module [main]

check : a, b -> {}
check = \_, _ -> {}

main =
    dbg (check (RStr "2024-01-15T10:30:00+00:00") (RStr "2024-06-01"))
    {}
