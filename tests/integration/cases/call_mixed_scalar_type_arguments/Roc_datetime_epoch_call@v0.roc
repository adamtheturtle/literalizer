module [main]

capture : a, b, c, d, e, f, g -> {}
capture = \_, _, _, _, _, _, _ -> {}

main =
    dbg (capture (RFloat Num.nan_f64) (RFloat Num.infinity_f64) (RFloat -Num.infinity_f64) (RFloat 1.25) (RStr "2024-01-15") (RInt 1705322096i128) (RStr "[ordinary text]"))
    {}
