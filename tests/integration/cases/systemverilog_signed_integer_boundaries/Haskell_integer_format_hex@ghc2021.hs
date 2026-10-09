module Fixture_systemverilog_signed_integer_boundaries_Haskell_integer_format_hex where
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
    ("i32_below", -0x80000001),
    ("i32_minimum", -0x80000000),
    ("i32_above", -0x7fffffff),
    ("i32_maximum", 0x7fffffff),
    ("i32_over", 0x80000000),
    ("i64_minimum", -0x8000000000000000),
    ("i64_maximum", 0x7fffffffffffffff)
    ]
main :: IO ()
main = seq my_data (return ())
