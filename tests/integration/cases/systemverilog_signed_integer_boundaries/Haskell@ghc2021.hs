module Fixture_systemverilog_signed_integer_boundaries_Haskell where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("i32_below", -2147483649),
    ("i32_minimum", -2147483648),
    ("i32_above", -2147483647),
    ("i32_maximum", 2147483647),
    ("i32_over", 2147483648),
    ("i64_minimum", -9223372036854775808),
    ("i64_maximum", 9223372036854775807)
    ]
main :: IO ()
main = seq my_data (return ())
